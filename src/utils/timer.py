# timer.py (Gradio compatible)
"""
Timer utilities for managing test round timers (Gradio Version).
Manages timing using the shared state dictionary.
"""

import time
from typing import Dict, Any


# ------------------ Timer Core Logic ------------------

def start_timer(state: Dict[str, Any], duration_seconds: int) -> Dict[str, Any]:
    """Start a timer by writing into state."""
    now = time.time()
    state["timer_start"] = now
    state["timer_duration"] = duration_seconds
    state["timer_end"] = now + duration_seconds
    return state


def get_remaining_time(state: Dict[str, Any]) -> float:
    """Return remaining time in seconds."""
    if "timer_end" not in state:
        return 0
    return max(0, state["timer_end"] - time.time())


def reset_timer(state: Dict[str, Any]) -> Dict[str, Any]:
    """Remove all timer data from state."""
    for key in ("timer_start", "timer_duration", "timer_end"):
        if key in state:
            del state[key]
    return state


def format_time(seconds: float) -> str:
    """Convert seconds → MM:SS formatted string."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def get_elapsed_time(state: Dict[str, Any]) -> float:
    """Return elapsed time since timer started."""
    if "timer_start" not in state:
        return 0
    return time.time() - state["timer_start"]


# ------------------ UI Helper (HTML for Gradio) ------------------

def render_timer_html(state: Dict[str, Any], auto_submit: bool = True):
    """
    Returns:
        (updated_state, timer_html: str, time_up: bool)
    """
    remaining = get_remaining_time(state)
    duration = state.get("timer_duration", 180)
    progress = remaining / duration if duration > 0 else 0

    # Choose bar color (same logic as your Streamlit version)
    if remaining > duration * 0.5:
        color = "#4F46E5"  # blue
    elif remaining > duration * 0.25:
        color = "#f59e0b"  # orange
    else:
        color = "#ef4444"  # red

    time_str = format_time(remaining)

    timer_html = f"""
    <div style='
        width: 100%;
        height: 6px;
        background-color: #e5e7eb;
        border-radius: 3px;
        margin-top: 6px;
    '>
        <div style='
            width: {progress * 100}%;
            height: 100%;
            background: {color};
            border-radius: 3px;
            transition: width 0.25s ease;
        '></div>
    </div>

    <div style='
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        color: {color};
        font-family: monospace;
        margin-top: 8px;
    '>
        {time_str}
    </div>
    """

    # Auto-submit trigger
    time_up = remaining <= 0

    return state, timer_html, (auto_submit and time_up)
