import json
import re
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path("/app/sessions")

_COMPETENCY_KEYS = [
    "Technical Knowledge",
    "Communication & Clarity",
    "Problem Solving",
    "Relevant Experience",
    "Role Fit",
]


def _parse_score(feedback: str) -> int | None:
    m = re.search(r"Overall Score:\s*(\d+)\s*/\s*10", feedback, re.IGNORECASE)
    return int(m.group(1)) if m else None


def _parse_competency_scores(feedback: str) -> dict[str, int]:
    """Extract individual competency scores from feedback markdown."""
    pattern = re.compile(r"\*\*(.+?)\s*[—–\-]+\s*(\d+)/10\*\*", re.IGNORECASE)
    scores = {}
    for m in pattern.finditer(feedback):
        name = m.group(1).strip()
        # Match against known keys (fuzzy: ignore case, allow partial)
        for key in _COMPETENCY_KEYS:
            if key.lower() in name.lower() or name.lower() in key.lower():
                scores[key] = int(m.group(2))
                break
    return scores


def save_session(
    role: str,
    industry: str,
    num_questions: int,
    transcript: list[dict],
    feedback: str | None,
    difficulty: str = "Medium",
    interview_format: str = "Mixed",
) -> str:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    session = {
        "id": session_id,
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "industry": industry,
        "num_questions": num_questions,
        "difficulty": difficulty,
        "interview_format": interview_format,
        "transcript": transcript,
        "feedback": feedback,
        "score": _parse_score(feedback) if feedback else None,
        "competency_scores": _parse_competency_scores(feedback) if feedback else {},
    }
    (SESSIONS_DIR / f"{session_id}.json").write_text(
        json.dumps(session, indent=2, ensure_ascii=False)
    )
    return session_id


def load_sessions() -> list[dict]:
    if not SESSIONS_DIR.exists():
        return []
    sessions = []
    for f in sorted(SESSIONS_DIR.glob("*.json"), reverse=True):
        try:
            s = json.loads(f.read_text())
            # Back-fill competency scores for older sessions that lack them
            if s.get("feedback") and not s.get("competency_scores"):
                s["competency_scores"] = _parse_competency_scores(s["feedback"])
            sessions.append(s)
        except Exception:
            pass
    return sessions


def delete_session(session_id: str) -> None:
    path = SESSIONS_DIR / f"{session_id}.json"
    if path.exists():
        path.unlink()
