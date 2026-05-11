import io
import requests
import streamlit as st
from fpdf import FPDF

from cv_parser import extract_text_from_pdf
from agent import InterviewAgent, OLLAMA_BASE_URL
from demo_data import DEMO_SCENARIOS
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from session_store import save_session, load_sessions, delete_session, _COMPETENCY_KEYS

st.set_page_config(page_title="AI Interview Agent", page_icon="🎙️", layout="centered")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_ollama_models() -> list[str]:
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
        return models if models else ["llama3.2"]
    except Exception:
        return ["llama3.2"]


def _latin1(text: str) -> str:
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _pdf_heading(pdf: FPDF, text: str, w: float, size: int = 13) -> None:
    pdf.set_font("Helvetica", "B", size)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 8, _latin1(text), align="L", new_x="LMARGIN", new_y="NEXT")


def _pdf_body(pdf: FPDF, text: str, w: float) -> None:
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, 6, _latin1(text), align="L", new_x="LMARGIN", new_y="NEXT")


def build_pdf(transcript: list[dict], role: str, feedback: str | None = None) -> bytes:
    pdf = FPDF()
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=20)
    w = pdf.w - pdf.l_margin - pdf.r_margin

    if feedback:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_x(pdf.l_margin)
        pdf.cell(w, 12, "Interview Feedback Report", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_x(pdf.l_margin)
        pdf.cell(w, 8, _latin1(f"Role: {role}"), align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)
        for line in feedback.splitlines():
            s = line.strip()
            if not s:
                pdf.ln(3)
            elif s.startswith("## "):
                pdf.ln(2); _pdf_heading(pdf, s[3:], w, size=14); pdf.ln(1)
            elif s.startswith("### "):
                pdf.ln(2); _pdf_heading(pdf, s[4:], w, size=12)
            elif s.startswith("**") and s.endswith("**"):
                _pdf_heading(pdf, s.strip("*"), w, size=11)
            else:
                _pdf_body(pdf, s, w)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_x(pdf.l_margin)
    pdf.cell(w, 12, "Interview Transcript", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_x(pdf.l_margin)
    pdf.cell(w, 8, _latin1(f"Role: {role}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    for entry in transcript:
        _pdf_heading(pdf, entry["role"] + ":", w, size=11)
        _pdf_body(pdf, entry["content"], w)
        pdf.ln(4)

    return bytes(pdf.output())


def reset_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def _render_bubble(entry: dict) -> None:
    if entry["role"] == "Interviewer":
        st.markdown(
            f'<div class="interviewer-bubble">'
            f'<div class="bubble-label">Interviewer</div>{entry["content"]}'
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="candidate-bubble">'
            f'<div class="bubble-label">You</div>{entry["content"]}'
            f"</div>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

def init_state():
    defaults = {
        "stage": "setup",
        "agent": None,
        "cv_text": "",
        "role": "",
        "num_questions": 10,
        "model": "llama3.2",
        "chat_history": [],
        "followup_history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    .interviewer-bubble {
        background: #1e3a5f;
        color: #e8f0fe;
        border-radius: 12px 12px 12px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
        max-width: 85%;
    }
    .candidate-bubble {
        background: #2d6a4f;
        color: #d8f3dc;
        border-radius: 12px 12px 0 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        max-width: 85%;
        margin-left: auto;
    }
    .bubble-label {
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 4px;
        opacity: 0.75;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Stage 1 — Setup
# ---------------------------------------------------------------------------

def render_setup():
    st.title("AI Interview Agent")
    st.markdown(
        "Upload your CV, enter the role you're applying for, and practise a "
        "realistic mock interview powered by a local LLM."
    )
    st.divider()

    available_models = fetch_ollama_models()

    tab_new, tab_history, tab_progress = st.tabs(["New Interview", "Past Sessions", "Progress"])

    with tab_new:
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])
        with col2:
            role = st.text_input("Target job role", placeholder="e.g. Senior React Developer")

        col3, col4 = st.columns(2)
        with col3:
            industry = st.text_input(
                "Industry",
                placeholder="e.g. Software Development, Healthcare, Finance",
            )
        with col4:
            model = st.selectbox("Ollama model", options=available_models, index=0)

        col5, col6 = st.columns(2)
        with col5:
            difficulty = st.radio(
                "Difficulty",
                options=["Easy", "Medium", "Hard"],
                index=1,
                horizontal=True,
            )
        with col6:
            interview_format = st.selectbox(
                "Interview format",
                options=["Mixed", "Phone Screen", "Technical Deep-Dive", "Behavioural Panel", "Final Round"],
            )

        job_description = st.text_area(
            "Job description (optional — paste the JD for more targeted questions)",
            height=160,
            placeholder="Paste the full job description here…",
        )

        num_questions = st.slider(
            "Number of interview questions", min_value=5, max_value=20, value=10
        )

        ready = uploaded_file is not None and role.strip() != ""
        start_btn = st.button("Start Interview", disabled=not ready, type="primary")

        if start_btn and ready:
            with st.spinner("Parsing CV and initialising interviewer…"):
                try:
                    cv_text = extract_text_from_pdf(uploaded_file)
                except ValueError:
                    st.error(
                        "Could not extract text from this PDF — it may be scanned or "
                        "image-based. Please try a text-based PDF."
                    )
                    return
                except Exception as e:
                    st.error(f"PDF parsing error: {e}")
                    return

                agent = InterviewAgent(
                    cv_text=cv_text,
                    role=role.strip(),
                    industry=industry.strip(),
                    job_description=job_description.strip(),
                    num_questions=num_questions,
                    model=model,
                    difficulty=difficulty,
                    interview_format=interview_format,
                )

                try:
                    opening = agent.start()
                except Exception as e:
                    st.error(
                        f"Could not reach Ollama. Make sure it is running and that "
                        f"the model `{model}` is pulled.\n\nError: {e}"
                    )
                    return

                st.session_state.agent = agent
                st.session_state.cv_text = cv_text
                st.session_state.role = role.strip()
                st.session_state.industry = industry.strip()
                st.session_state.num_questions = num_questions
                st.session_state.model = model
                st.session_state.difficulty = difficulty
                st.session_state.interview_format = interview_format
                st.session_state.chat_history = [
                    {"role": "Interviewer", "content": opening}
                ]
                st.session_state.stage = "interview"
                st.rerun()

        # Demo mode
        st.divider()
        st.markdown("#### Try a demo interview")
        st.caption(
            "Skip straight to the feedback screen using a pre-written transcript. "
            "The AI feedback report is still generated live."
        )

        demo_choice = st.selectbox(
            "Choose a scenario",
            options=list(DEMO_SCENARIOS.keys()),
            label_visibility="collapsed",
        )

        # Scenario info card
        scenario_meta = DEMO_SCENARIOS[demo_choice]
        diff_colour = {"Easy": "#27ae60", "Medium": "#e67e22", "Hard": "#c0392b"}.get(
            scenario_meta.get("difficulty", "Medium"), "#888"
        )
        st.markdown(
            f"""<div style="background:#1a1a2e;border-radius:8px;padding:12px 16px;margin:6px 0 10px 0">
<span style="background:{diff_colour};color:white;border-radius:4px;padding:2px 8px;
font-size:0.72rem;font-weight:700;margin-right:8px">{scenario_meta.get("difficulty","Medium")}</span>
<span style="background:#2d4a7a;color:#aac4ff;border-radius:4px;padding:2px 8px;
font-size:0.72rem;font-weight:700">{scenario_meta.get("interview_format","Mixed")}</span>
<div style="margin-top:8px;color:#ccc;font-size:0.88rem">{scenario_meta.get("description","")}</div>
</div>""",
            unsafe_allow_html=True,
        )

        demo_col1, demo_col2 = st.columns([3, 1])
        with demo_col1:
            diff_override = st.radio(
                "Difficulty override",
                options=["Default", "Easy", "Medium", "Hard"],
                index=0,
                horizontal=True,
                help="Override the scenario's default difficulty level for the feedback report.",
            )
        with demo_col2:
            st.write("")
            if st.button("Load Demo", type="secondary"):
                effective_diff = None if diff_override == "Default" else diff_override
                _load_demo(demo_choice, model, difficulty_override=effective_diff)

    with tab_history:
        render_sessions()

    with tab_progress:
        render_progress()


def render_sessions():
    sessions = load_sessions()
    if not sessions:
        st.info("No past interviews yet. Complete an interview to see your history here.")
        return

    for s in sessions:
        score_str = f"{s['score']}/10" if s.get("score") else "N/A"
        industry_str = f" · {s['industry']}" if s.get("industry") else ""
        label = f"{s['role']}{industry_str} — {s['timestamp'][:10]} — Score: {score_str}"

        with st.expander(label):
            if s.get("feedback"):
                st.markdown(s["feedback"])
            else:
                st.info("No feedback available for this session.")

            if st.button("Delete", key=f"del_{s['id']}"):
                delete_session(s["id"])
                st.rerun()


def render_progress():
    sessions = load_sessions()
    scored = [s for s in sessions if s.get("score") is not None]

    if not scored:
        st.info("Complete at least one interview to see your progress charts here.")
        return

    # ── Overall score over time ───────────────────────────────────────────────
    st.subheader("Overall Score Over Time")
    df = pd.DataFrame([
        {
            "Date": s["timestamp"][:10],
            "Score": s["score"],
            "Role": s["role"],
            "Format": s.get("interview_format", "Mixed"),
            "Difficulty": s.get("difficulty", "Medium"),
        }
        for s in scored
    ])
    fig_line = px.line(
        df, x="Date", y="Score", color="Role", markers=True,
        labels={"Score": "Score / 10"},
        range_y=[0, 10],
    )
    fig_line.update_traces(marker_size=8)
    fig_line.update_layout(legend_title_text="Role", hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

    # ── Summary stats ─────────────────────────────────────────────────────────
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Interviews completed", len(sessions))
    col_b.metric("Average score", f"{sum(s['score'] for s in scored) / len(scored):.1f} / 10")
    best = max(scored, key=lambda s: s["score"])
    col_c.metric("Best score", f"{best['score']} / 10", help=f"{best['role']} — {best['timestamp'][:10]}")

    # ── Competency radar ──────────────────────────────────────────────────────
    st.subheader("Average Competency Scores")
    st.caption("Averaged across all sessions that produced a detailed feedback report.")

    avg_competency: dict[str, float] = {}
    for key in _COMPETENCY_KEYS:
        vals = [
            s["competency_scores"][key]
            for s in sessions
            if s.get("competency_scores", {}).get(key) is not None
        ]
        if vals:
            avg_competency[key] = round(sum(vals) / len(vals), 1)

    if avg_competency:
        cats = list(avg_competency.keys())
        vals = list(avg_competency.values())
        fig_radar = go.Figure(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            line_color="#4a90d9",
            fillcolor="rgba(74,144,217,0.25)",
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10], tickvals=list(range(0, 11, 2)))),
            showlegend=False,
            margin=dict(t=20, b=20, l=40, r=40),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Competency bar breakdown
        bar_df = pd.DataFrame({"Competency": cats, "Average Score": vals})
        fig_bar = px.bar(
            bar_df, x="Average Score", y="Competency", orientation="h",
            range_x=[0, 10], color="Average Score",
            color_continuous_scale=["#c0392b", "#e67e22", "#27ae60"],
            range_color=[0, 10],
        )
        fig_bar.update_layout(coloraxis_showscale=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Competency scores will appear here once your feedback reports are generated.")

    # ── Difficulty / format breakdown ─────────────────────────────────────────
    if len(scored) >= 2:
        st.subheader("Score by Difficulty & Format")
        col_d, col_f = st.columns(2)
        with col_d:
            diff_df = df.groupby("Difficulty")["Score"].mean().reset_index()
            diff_df.columns = ["Difficulty", "Avg Score"]
            st.dataframe(diff_df, hide_index=True, use_container_width=True)
        with col_f:
            fmt_df = df.groupby("Format")["Score"].mean().reset_index()
            fmt_df.columns = ["Format", "Avg Score"]
            st.dataframe(fmt_df, hide_index=True, use_container_width=True)


def _load_demo(scenario_name: str, model: str, difficulty_override: str | None = None) -> None:
    scenario = DEMO_SCENARIOS[scenario_name]
    from langchain_core.messages import HumanMessage, AIMessage

    difficulty = difficulty_override or scenario.get("difficulty", "Medium")
    interview_format = scenario.get("interview_format", "Mixed")

    agent = InterviewAgent(
        cv_text=scenario["cv_text"],
        role=scenario["role"],
        industry=scenario["industry"],
        job_description=scenario["job_description"],
        num_questions=len(scenario["exchanges"]),
        model=model,
        difficulty=difficulty,
        interview_format=interview_format,
    )

    chat_history = []
    for ex in scenario["exchanges"]:
        agent._messages.append(AIMessage(content=ex["question"]))
        agent._messages.append(HumanMessage(content=ex["answer"]))
        chat_history.append({"role": "Interviewer", "content": ex["question"]})
        chat_history.append({"role": "You", "content": ex["answer"]})

    agent.question_count = len(scenario["exchanges"])
    agent.is_complete = True

    closing = (
        "Thank you so much for your time today — it's been a really enjoyable conversation. "
        "We'll be in touch shortly. Your feedback report is being prepared now."
    )
    agent._messages.append(AIMessage(content=closing))
    chat_history.append({"role": "Interviewer", "content": closing})

    st.session_state.agent = agent
    st.session_state.role = scenario["role"]
    st.session_state.industry = scenario["industry"]
    st.session_state.num_questions = len(scenario["exchanges"])
    st.session_state.model = model
    st.session_state.difficulty = difficulty
    st.session_state.interview_format = interview_format
    st.session_state.chat_history = chat_history
    st.session_state.followup_history = []
    st.session_state.stage = "complete"
    st.rerun()


# ---------------------------------------------------------------------------
# Stage 2 — Interview
# ---------------------------------------------------------------------------

def render_interview():
    # Clear answer widget state before it's instantiated
    if st.session_state.pop("clear_answer", False):
        st.session_state.pop("answer_box", None)

    agent: InterviewAgent = st.session_state.agent
    role = st.session_state.role
    num_questions = st.session_state.num_questions
    q_count = min(agent.question_count, num_questions)

    col_title, col_counter = st.columns([3, 1])
    with col_title:
        st.subheader(f"Interview: {role}")
    with col_counter:
        st.metric("Question", f"{q_count} / {num_questions}")

    st.progress(min(q_count / num_questions, 1.0))
    st.divider()

    # Chat history
    for entry in st.session_state.chat_history:
        _render_bubble(entry)

    # Stream pending reply (runs immediately after history, no input shown while streaming)
    if st.session_state.pop("needs_reply", False):
        last_answer = st.session_state.chat_history[-1]["content"]
        placeholder = st.empty()
        accumulated = ""
        try:
            for chunk in agent.stream_reply(last_answer):
                accumulated += chunk
                placeholder.markdown(
                    f'<div class="interviewer-bubble">'
                    f'<div class="bubble-label">Interviewer</div>'
                    f"{accumulated}▌</div>",
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.error(f"LLM error: {e}")
            return
        placeholder.markdown(
            f'<div class="interviewer-bubble">'
            f'<div class="bubble-label">Interviewer</div>'
            f"{accumulated}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.chat_history.append({"role": "Interviewer", "content": accumulated})
        st.rerun()
        return

    st.divider()

    if agent.is_complete:
        st.session_state.stage = "complete"
        st.rerun()
        return

    answer = st.text_area(
        "Your answer", height=140, key="answer_box",
        placeholder="Type your answer here…"
    )

    col_submit, col_end = st.columns([2, 1])
    with col_submit:
        submit = st.button("Submit Answer", type="primary", disabled=answer.strip() == "")
    with col_end:
        end_early = st.button("End Interview Early")

    if submit and answer.strip():
        st.session_state.chat_history.append({"role": "You", "content": answer.strip()})
        st.session_state["needs_reply"] = True
        st.session_state["clear_answer"] = True
        st.rerun()

    if end_early:
        with st.spinner("Wrapping up…"):
            try:
                closing = agent.force_end()
            except Exception as e:
                st.error(f"LLM error: {e}")
                return
            st.session_state.chat_history.append({"role": "Interviewer", "content": closing})
        st.session_state.stage = "complete"
        st.rerun()


# ---------------------------------------------------------------------------
# Stage 3 — Complete
# ---------------------------------------------------------------------------

def render_complete():
    agent: InterviewAgent = st.session_state.agent
    role = st.session_state.role

    st.title("Interview Complete")
    st.success("Well done for completing the interview!")

    # Generate and cache feedback
    if "feedback_report" not in st.session_state:
        with st.spinner("Analysing your interview and generating feedback report…"):
            try:
                st.session_state.feedback_report = agent.generate_feedback()
            except Exception as e:
                st.session_state.feedback_report = None
                st.error(f"Could not generate feedback: {e}")

    # Save session once
    if not st.session_state.get("session_saved"):
        try:
            save_session(
                role=role,
                industry=st.session_state.get("industry", ""),
                num_questions=st.session_state.get("num_questions", 0),
                transcript=agent.get_transcript(),
                feedback=st.session_state.get("feedback_report"),
                difficulty=st.session_state.get("difficulty", "Medium"),
                interview_format=st.session_state.get("interview_format", "Mixed"),
            )
            st.session_state.session_saved = True
        except Exception:
            pass  # session saving is non-critical

    # Feedback report
    feedback = st.session_state.get("feedback_report")
    if feedback:
        st.divider()
        st.subheader("Feedback Report")
        st.markdown(feedback)

    # Transcript (collapsed)
    st.divider()
    with st.expander("View full interview transcript", expanded=False):
        for entry in st.session_state.chat_history:
            _render_bubble(entry)

    st.divider()

    col_dl, col_new = st.columns(2)
    with col_dl:
        try:
            pdf_bytes = build_pdf(agent.get_transcript(), role, feedback)
            st.download_button(
                label="Download Report (PDF)",
                data=io.BytesIO(pdf_bytes),
                file_name="interview_report.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.warning(f"PDF export unavailable: {e}")
    with col_new:
        if st.button("Start New Interview", type="primary"):
            reset_state()
            st.rerun()

    # Follow-up coaching chat
    if feedback:
        st.divider()
        st.subheader("Ask your feedback coach")
        st.caption(
            "Ask anything about your feedback — "
            "'What would a stronger answer to Q2 have looked like?' "
            "or 'How can I improve my behavioural answers?'"
        )

        for msg in st.session_state.followup_history:
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                st.markdown(msg["content"])

        if user_q := st.chat_input("Ask about your feedback…"):
            st.session_state.followup_history.append({"role": "user", "content": user_q})
            with st.chat_message("user"):
                st.markdown(user_q)
            with st.chat_message("assistant"):
                response = st.write_stream(
                    agent.stream_followup(
                        feedback=feedback,
                        history=st.session_state.followup_history,
                    )
                )
            st.session_state.followup_history.append({"role": "assistant", "content": response})


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

if st.session_state.stage == "setup":
    render_setup()
elif st.session_state.stage == "interview":
    render_interview()
elif st.session_state.stage == "complete":
    render_complete()
