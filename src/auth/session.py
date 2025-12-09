# auth/session.py  (GRADIO VERSION - FINAL)

from datetime import datetime
from typing import Dict, Any, Optional, List

# Fixed round order used throughout the platform
VALID_ROUNDS = ["aptitude", "listening", "reading"]


# ---------------------------------------------------------
#  SESSION INITIALIZATION
# ---------------------------------------------------------
def initialize_session_state() -> Dict[str, Any]:
    """Return a clean default Gradio state dictionary."""
    
    return {
        # ---- User Info ----
        "user_name": None,
        "difficulty": "Easy",
        "name_submitted": False,

        # ---- Navigation ----
        "current_page": "setup",     # setup → aptitude → listening → reading → results
        "current_round": None,
        "test_started": False,
        "test_complete": False,

        # ---- Timing ----
        "session_start": None,
        "test_start_time": None,
        "test_end_time": None,

        # ---- Round completion tracking ----
        "rounds_completed": [],

        # ---- Aptitude round ----
        "aptitude_questions": [],
        "current_question_index": 0,
        "aptitude_score": 0,
        "aptitude_answers": [],

        # ---- Listening round ----
        "listening_content": None,
        "audio_played": False,
        "listening_score": 0,
        "listening_answers": [],

        # ---- Reading round ----
        "reading_content": None,
        "reading_start_time": None,
        "summary_text": "",
        "summary_submitted": False,
        "reading_score": 0,

        # ---- Final scoring ----
        "scores": {
            "aptitude": 0,
            "listening": 0,
            "reading": 0
        }
    }


# ---------------------------------------------------------
#  SESSION RESET
# ---------------------------------------------------------
def reset_session() -> Dict[str, Any]:
    """Return a brand-new state when the user clicks Restart Test."""
    return initialize_session_state()


# ---------------------------------------------------------
#  START TEST
# ---------------------------------------------------------
def start_test(state: Dict[str, Any]) -> Dict[str, Any]:
    """Start a new test and set initial round to Aptitude."""
    new_state = state.copy()

    new_state["test_started"] = True
    new_state["session_start"] = datetime.now()
    new_state["current_round"] = "aptitude"
    new_state["current_page"] = "aptitude"

    new_state["rounds_completed"] = []
    new_state["scores"] = {"aptitude": 0, "listening": 0, "reading": 0}

    return new_state


# ---------------------------------------------------------
#  ROUND TRANSITION LOGIC
# ---------------------------------------------------------
def complete_round(state: Dict[str, Any], round_name: str) -> Dict[str, Any]:
    """Mark a round complete and transition to the next."""
    
    new_state = state.copy()

    if round_name not in VALID_ROUNDS:
        return new_state

    # Mark round as completed
    if round_name not in new_state["rounds_completed"]:
        new_state["rounds_completed"].append(round_name)

    # Determine next round
    index = VALID_ROUNDS.index(round_name)

    if index < len(VALID_ROUNDS) - 1:
        next_round = VALID_ROUNDS[index + 1]
        new_state["current_round"] = next_round
        new_state["current_page"] = next_round
    else:
        # All rounds done → go to results
        new_state["current_round"] = "complete"
        new_state["current_page"] = "results"
        new_state["test_complete"] = True

    return new_state


def get_next_round(state: Dict[str, Any]) -> Optional[str]:
    """Return the next round based on the current state."""
    current = state.get("current_round")

    if not current or current == "complete":
        return None

    try:
        idx = VALID_ROUNDS.index(current)
        if idx < len(VALID_ROUNDS) - 1:
            return VALID_ROUNDS[idx + 1]
    except ValueError:
        return None

    return None


# ---------------------------------------------------------
#  VALIDATION
# ---------------------------------------------------------
def validate_state(state: Dict[str, Any]) -> bool:
    """Basic internal state validator for debugging."""
    try:
        if state.get("test_started"):
            assert state.get("user_name"), "User name missing"
            assert state.get("difficulty"), "Difficulty missing"
            assert state.get("session_start"), "Session start time missing"

            current_round = state.get("current_round")
            assert current_round, "Current round not set"

            if current_round != "complete":
                assert current_round in VALID_ROUNDS, f"Invalid round: {current_round}"
                assert state.get("current_page") == current_round, "Page/round mismatch"

            completed = state.get("rounds_completed", [])
            assert all(r in VALID_ROUNDS for r in completed), "Invalid completed round entry"

        return True

    except AssertionError:
        return False


# ---------------------------------------------------------
#  PERFORMANCE SUMMARY (RESULTS)
# ---------------------------------------------------------
def get_performance_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    """Compute total score & result summary."""
    
    scores = state.get("scores", {})
    total_score = sum(scores.values())
    max_score = 15  # Adjust if you change scoring rules
    
    duration = None
    if state.get("session_start"):
        duration = (datetime.now() - state["session_start"]).total_seconds()

    return {
        "total_score": total_score,
        "max_score": max_score,
        "percentage": (total_score / max_score) * 100 if max_score else 0,
        "duration_seconds": duration,
        "scores_by_round": scores,
        "completed_rounds": state.get("rounds_completed", []),
        "test_complete": state.get("test_complete", False),
    }
