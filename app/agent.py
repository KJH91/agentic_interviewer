import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

OLLAMA_BASE_URL = "http://host.docker.internal:11434"

_STRIP_PATTERNS = [
    re.compile(r"\(I['']ll keep track[^)]*\)", re.IGNORECASE),
    re.compile(r"\(Count:.*?\)", re.IGNORECASE),
    re.compile(r"\(Question \d+ of \d+[^)]*\)", re.IGNORECASE),
    re.compile(r"\[Question \d+.*?\]", re.IGNORECASE),
]


_DIFFICULTY_INSTRUCTIONS: dict[str, str] = {
    "Easy": (
        "Interviewer style — Easy: Be warm, patient, and encouraging throughout. "
        "Ask clear, accessible questions. If the candidate gives a short or vague answer, "
        "offer one gentle prompt then move on. Create a supportive, low-pressure atmosphere."
    ),
    "Medium": (
        "Interviewer style — Medium: Be professional and balanced. "
        "Probe vague answers once before moving on. Maintain fair but reasonable expectations."
    ),
    "Hard": (
        "Interviewer style — Hard: Be direct and demanding. "
        "Push back on every vague or surface-level answer — ask for specific metrics, outcomes, and evidence. "
        "Play devil's advocate where appropriate. Do not accept one-line answers; probe for depth every time."
    ),
}

_FORMAT_INSTRUCTIONS: dict[str, str] = {
    "Mixed": (
        "Question format — Mixed: Ask a balanced spread of background/experience, "
        "technical, behavioural, and situational questions."
    ),
    "Phone Screen": (
        "Question format — Phone Screen: This is an initial screening call. "
        "Keep questions broad and conversational. Focus on career background, motivation for applying, "
        "and basic role fit. Avoid deep technical questions — this is about first impressions and fit."
    ),
    "Technical Deep-Dive": (
        "Question format — Technical Deep-Dive: Focus heavily on technical skills, architecture decisions, "
        "problem-solving approaches, and practical hands-on experience. Reference specific technologies "
        "from the CV. Include system design or scenario-based questions ('How would you design...'). "
        "Minimal behavioural content — prioritise technical depth."
    ),
    "Behavioural Panel": (
        "Question format — Behavioural Panel: Ask exclusively STAR-format questions "
        "('Tell me about a time when...', 'Give me an example of...', 'Describe a situation where...'). "
        "Probe for Situation, Task, Action, and Result in every answer. "
        "Cover: teamwork, conflict resolution, leadership, handling failure, and notable achievements. "
        "No technical questions."
    ),
    "Final Round": (
        "Question format — Final Round: The candidate has already passed technical screening. "
        "Focus on strategic thinking, cultural fit, values alignment, leadership style, and long-term vision. "
        "Include scenario-based questions ('What would you do if...'). "
        "This is the most important stage — be thorough and probe deeply."
    ),
}


def _build_system_prompt(
    cv_text: str,
    role: str,
    industry: str,
    job_description: str,
    num_questions: int,
    difficulty: str = "Medium",
    interview_format: str = "Mixed",
) -> str:
    if industry:
        persona = (
            f"You are an experienced interviewer in the {industry} industry conducting "
            f"a job interview for a {role} position. Adopt the persona of a senior professional "
            f"appropriate for that industry (e.g. Tech Lead for software, Senior Nurse for healthcare, "
            f"Finance Manager for finance)."
        )
    else:
        persona = (
            f"You are an experienced professional interviewer conducting a job "
            f"interview for a {role} position."
        )

    jd_section = f"\nJob Description:\n{job_description}\n" if job_description else ""
    difficulty_line = _DIFFICULTY_INSTRUCTIONS.get(difficulty, _DIFFICULTY_INSTRUCTIONS["Medium"])
    format_line = _FORMAT_INSTRUCTIONS.get(interview_format, _FORMAT_INSTRUCTIONS["Mixed"])

    return f"""You are conducting a structured job interview. You speak only as yourself — never generate text on behalf of the candidate.

{persona}

Candidate CV:
{cv_text}
{jd_section}
Target Role: {role}
Total questions to ask: {num_questions}

{difficulty_line}

{format_line}

Rules:
- Respond with your interviewer turn only. Stop writing the moment your turn ends.
- Ask exactly ONE question per response. Never ask two questions in the same message.
- Reference something specific from the CV, the job description (if provided), or the target role in every question.
- Where a job description is provided, prioritise probing the candidate against its specific requirements.
- Never repeat a topic already covered.
- Do not narrate your internal state. Do not write things like "(I'll keep track...)" or "(Count: X/Y)".
- When the system tells you all questions are done, give a brief, warm closing — thank the candidate and let them know feedback will follow. Do not attempt to write the feedback yourself."""


def _build_feedback_prompt(
    cv_text: str,
    role: str,
    industry: str,
    job_description: str,
    transcript: str,
) -> str:
    industry_line = f"Industry: {industry}" if industry else ""
    jd_section = f"\nJob Description:\n{job_description}\n" if job_description else ""
    jd_instruction = (
        """### Job Description Gap Analysis

For each key requirement in the job description, assess how well the candidate evidenced it:

**Evidenced Well:**
- [Requirement] → [Specific evidence from the interview]

**Partially Evidenced:**
- [Requirement] → [What was shown and what was missing]

**Not Evidenced:**
- [Requirement] → [Why it matters and how to address it]"""
        if job_description
        else """### Job Description Gap Analysis

No job description was provided for this session."""
    )

    return f"""You are an expert interview coach. A job interview has just concluded. Your task is to write a comprehensive, honest, and constructive feedback report for the candidate.

Role: {role}
{industry_line}
{jd_section}
Candidate CV Summary:
{cv_text}

Interview Transcript:
{transcript}

Write the feedback report below. Be specific — reference actual things the candidate said. Do not be vague or generic.

---

## Interview Feedback Report

### Overall Score: X/10
[One sentence honest summary of overall performance]

---

### Competency Scorecard

Score each competency 1–10 based only on evidence from this interview:

**Technical Knowledge — X/10**
[1–2 sentences. Reference a specific answer that supports the score.]

**Communication & Clarity — X/10**
[1–2 sentences. Was the candidate clear, structured, concise?]

**Problem Solving — X/10**
[1–2 sentences. Did they demonstrate structured thinking when facing challenges?]

**Relevant Experience — X/10**
[1–2 sentences. How well did their experience map to the role requirements?]

**Role Fit — X/10**
[1–2 sentences. Based on the interview overall, how well do they fit this role?]

---

{jd_instruction}

---

### Per-Question Review

For every question asked, provide a brief review of the candidate's answer:

**Q: [Summarise the question in one sentence]**
- **Strength:** [What they did well in this answer]
- **Gap:** [What was weak, missing, or vague]
- **Tip:** [One concrete, specific thing they can do to give a stronger answer next time]

[Repeat for each question]

---

### Key Strengths
- [Specific strength with evidence]
- [Specific strength with evidence]
- [Specific strength with evidence]

### Priority Areas to Improve
- [Specific area with actionable advice]
- [Specific area with actionable advice]
- [Specific area with actionable advice]

### Recommended Next Steps
1. [Concrete action — e.g. study a specific topic, practise a specific answer type]
2. [Concrete action]
3. [Concrete action]
4. [Concrete action]
5. [Concrete action]"""


class InterviewAgent:
    def __init__(
        self,
        cv_text: str,
        role: str,
        num_questions: int,
        model: str,
        industry: str = "",
        job_description: str = "",
        difficulty: str = "Medium",
        interview_format: str = "Mixed",
    ):
        self.cv_text = cv_text
        self.role = role
        self.num_questions = num_questions
        self.model = model
        self.industry = industry
        self.job_description = job_description
        self.difficulty = difficulty
        self.interview_format = interview_format
        self.question_count = 0
        self.is_complete = False

        self._messages: list = []

        self.llm = ChatOllama(
            model=model,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7,
            stop=["Candidate:", "\nCandidate", "You:", "\nYou:"],
        )

        self._system = SystemMessage(
            content=_build_system_prompt(
                cv_text=cv_text,
                role=role,
                industry=industry,
                job_description=job_description,
                num_questions=num_questions,
                difficulty=difficulty,
                interview_format=interview_format,
            )
        )

    def _clean(self, text: str) -> str:
        for marker in ("Candidate:", "You:", "\nCandidate", "\nYou:"):
            if marker in text:
                text = text[: text.index(marker)]
        for pattern in _STRIP_PATTERNS:
            text = pattern.sub("", text)
        return text.strip()

    def _invoke(self, extra: HumanMessage | None = None) -> str:
        messages = [self._system] + self._messages
        if extra:
            messages.append(extra)
        response = self.llm.invoke(messages)
        return self._clean(response.content)

    def start(self) -> str:
        directive = HumanMessage(
            content=(
                f"Begin the interview. Introduce yourself briefly, welcome the candidate, "
                f"and ask question 1 of {self.num_questions}. One question only. "
                "Do not write anything on behalf of the candidate."
            )
        )
        response = self._invoke(directive)
        self._messages.append(directive)
        self._messages.append(AIMessage(content=response))
        self.question_count = 1
        return response

    def _make_directive(self, is_final: bool) -> HumanMessage:
        if is_final:
            return HumanMessage(
                content=(
                    f"[That was the answer to question {self.question_count} of {self.num_questions}. "
                    "All questions are complete. Do NOT ask another question. "
                    "Give a brief, warm closing — thank the candidate by name if you know it, "
                    "and let them know their feedback report is being prepared. Keep it to 2–3 sentences.]"
                )
            )
        next_q = self.question_count + 1
        return HumanMessage(
            content=(
                f"[Question {self.question_count} answered. "
                f"Now ask question {next_q} of {self.num_questions}. "
                "One question only. Choose a topic not yet covered. "
                "Do not write anything on behalf of the candidate.]"
            )
        )

    def _finalise_reply(self, response: str) -> None:
        self._messages.append(AIMessage(content=response))
        self.question_count += 1
        if self.question_count > self.num_questions:
            self.is_complete = True

    def reply(self, candidate_answer: str) -> str:
        if not candidate_answer.strip():
            raise ValueError("Cannot process an empty answer.")
        self._messages.append(HumanMessage(content=candidate_answer))
        directive = self._make_directive(self.question_count >= self.num_questions)
        response = self._invoke(directive)
        self._finalise_reply(response)
        return response

    def stream_reply(self, candidate_answer: str):
        """Yield text chunks for the interviewer's next response, then update state."""
        if not candidate_answer.strip():
            raise ValueError("Cannot process an empty answer.")
        self._messages.append(HumanMessage(content=candidate_answer))
        directive = self._make_directive(self.question_count >= self.num_questions)
        messages = [self._system] + self._messages + [directive]

        accumulated = ""
        for chunk in self.llm.stream(messages):
            text = chunk.content
            accumulated += text
            yield text

        self._finalise_reply(self._clean(accumulated))

    def force_end(self) -> str:
        directive = HumanMessage(
            content=(
                "[The candidate has ended the interview early. "
                "Do NOT ask another question. Give a brief, warm closing and let them know "
                "their feedback report is being prepared based on what was discussed. 2–3 sentences only.]"
            )
        )
        response = self._invoke(directive)
        self._messages.append(AIMessage(content=response))
        self.is_complete = True
        return response

    def generate_feedback(self) -> str:
        """Make a dedicated LLM call to produce the full structured feedback report."""
        transcript_lines = []
        q_num = 0
        for msg in self._messages:
            if isinstance(msg, HumanMessage) and msg.content.startswith("["):
                continue
            if isinstance(msg, HumanMessage):
                transcript_lines.append(f"Candidate: {msg.content}")
            elif isinstance(msg, AIMessage):
                q_num += 1
                transcript_lines.append(f"Interviewer (Q{q_num}): {msg.content}")
        transcript = "\n\n".join(transcript_lines)

        prompt = _build_feedback_prompt(
            cv_text=self.cv_text,
            role=self.role,
            industry=self.industry,
            job_description=self.job_description,
            transcript=transcript,
        )

        feedback_llm = ChatOllama(
            model=self.model,
            base_url=OLLAMA_BASE_URL,
            temperature=0.3,
        )
        response = feedback_llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()

    def stream_followup(self, feedback: str, history: list[dict]):
        """Yield chunks for a follow-up coaching response about the feedback report."""
        industry_line = f"Industry: {self.industry}" if self.industry else ""
        coach_system = SystemMessage(
            content=(
                f"You are an expert interview coach. A candidate just completed a mock job interview "
                f"for the role of {self.role}. {industry_line}\n\n"
                f"Their feedback report:\n{feedback}\n\n"
                "Answer their questions about the feedback specifically and helpfully. "
                "Reference their actual answers when relevant. Be constructive and encouraging. "
                "Keep responses concise and actionable."
            )
        )
        messages = [coach_system]
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

        coach_llm = ChatOllama(
            model=self.model,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7,
        )
        for chunk in coach_llm.stream(messages):
            yield chunk.content

    def get_transcript(self) -> list[dict]:
        result = []
        for msg in self._messages:
            if isinstance(msg, HumanMessage) and msg.content.startswith("["):
                continue
            if isinstance(msg, HumanMessage):
                result.append({"role": "Candidate", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "Interviewer", "content": msg.content})
        return result
