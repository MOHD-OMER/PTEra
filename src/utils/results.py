# results.py (Beautiful Gradio version)
from typing import Dict, Any
import gradio as gr
from src.utils.scoring import calculate_final_score

# Mapping for nicer labels
SECTION_LABELS = {
    "aptitude": "Aptitude",
    "listening": "Listening",
    "reading": "Reading",
}

# ---------- Helper logic (pure Python, no UI) ----------

def _get_performance_level(percentage: float) -> str:
    if percentage >= 80:
        return "Excellent"
    elif percentage >= 60:
        return "Good"
    return "Needs Improvement"


def _generate_detailed_feedback(scores: Dict[str, int]) -> str:
    """Generate detailed HTML feedback for each section."""
    if not scores:
        return "<div>No scores available for detailed feedback.</div>"

    html = []
    for raw_key, score in scores.items():
        # Normalize key + label
        key = raw_key.lower()
        label = SECTION_LABELS.get(key, raw_key.title())
        percentage = (score / 5) * 100 if score is not None else 0

        if percentage >= 80:
            gradient = "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)"
            border = "#10b981"
            icon = "🌟"
            msg = "Excellent performance! You've demonstrated strong mastery in this area."
        elif percentage >= 60:
            gradient = "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"
            border = "#f59e0b"
            icon = "👍"
            msg = "Good work! Some room for improvement but generally solid performance."
        else:
            gradient = "linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)"
            border = "#ef4444"
            icon = "💪"
            msg = "This area needs more focus and practice to improve your skills."

        html.append(f"""
            <div style='background:{gradient};padding:1.25rem;border-radius:12px;
                        margin-bottom:1rem;border-left:5px solid {border};
                        box-shadow:0 4px 15px rgba(0,0,0,0.08);'>
                <div style='display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;'>
                    <span style='font-size:1.5rem;'>{icon}</span>
                    <strong style='color:#1a1a1a;font-size:1.1rem;'>{label}:</strong>
                    <span style='background:{border};color:white;padding:0.25rem 0.75rem;
                                 border-radius:12px;font-size:0.85rem;font-weight:700;'>
                        {score}/5 ({percentage:.0f}%)
                    </span>
                </div>
                <div style='color:#374151;font-size:0.95rem;line-height:1.5;margin-left:2.5rem;'>
                    {msg}
                </div>
            </div>
        """)

    return "".join(html)


def _generate_personalized_tips(scores: Dict[str, int], percentage: float) -> Dict[str, str]:
    """Generate personalized tips based on performance (uses lowercase keys)."""
    tips: Dict[str, str] = {}

    # Normalize keys to lowercase internally
    lower_scores = {k.lower(): v for k, v in scores.items()}

    aptitude_score = lower_scores.get("aptitude", 0)
    if aptitude_score < 3:
        tips["Aptitude"] = (
            "Focus on basic arithmetic and algebra. "
            "Practice 30 minutes daily with mental math exercises."
        )
    elif aptitude_score < 4:
        tips["Aptitude"] = (
            "Good foundation! Work on complex problem-solving "
            "and time management during calculations."
        )
    else:
        tips["Aptitude"] = (
            "Excellent aptitude skills! Maintain your edge with "
            "advanced problem-solving practice."
        )

    listening_score = lower_scores.get("listening", 0)
    if listening_score < 3:
        tips["Listening"] = (
            "Start with slow-paced English content. Use subtitles initially, "
            "then gradually remove them."
        )
    elif listening_score < 4:
        tips["Listening"] = (
            "Practice with varied accents and faster speech. "
            "Try news broadcasts and podcasts."
        )
    else:
        tips["Listening"] = (
            "Outstanding listening skills! Challenge yourself with technical "
            "content and rapid speech."
        )

    reading_score = lower_scores.get("reading", 0)
    if reading_score < 3:
        tips["Reading"] = (
            "Build vocabulary with graded readers. Focus on comprehension "
            "over speed initially."
        )
    elif reading_score < 4:
        tips["Reading"] = (
            "Expand to complex texts. Practice skimming and scanning "
            "techniques for efficiency."
        )
    else:
        tips["Reading"] = (
            "Excellent reading ability! Tackle academic papers and technical "
            "documents to stay sharp."
        )

    return tips


def _generate_study_plan(percentage: float, scores: Dict[str, int]) -> Dict[str, str]:
    """Generate a personalized study plan based on performance percentage."""
    if percentage >= 80:
        return {
            "Daily Practice": "45–60 minutes maintenance study",
            "Weekly Schedule": "3–4 days focused practice",
            "Key Focus": "Advanced topics and maintaining current level",
            "Practice Tests": "One full test every 2 weeks",
        }
    elif percentage >= 60:
        return {
            "Daily Practice": "1–1.5 hours structured study",
            "Weekly Schedule": "5 days consistent practice",
            "Key Focus": "Strengthen weak areas while maintaining strong sections",
            "Practice Tests": "One full mock test weekly",
        }
    else:
        return {
            "Daily Practice": "2–2.5 hours intensive study",
            "Weekly Schedule": "6 days focused practice with one rest day",
            "Key Focus": "Foundation building in all areas with extra attention to weakest sections",
            "Practice Tests": "Two practice sessions weekly plus one full test",
        }


def _render_results_html(state: Dict[str, Any]) -> tuple[str, str, str]:
    """
    Build the three HTML blocks:
    - Performance Analysis
    - Personalized Tips
    - Study Plan

    Uses `state["scores"]` (expected keys: 'aptitude', 'listening', 'reading').
    """
    scores = state.get("scores", {}) or {}

    # Ensure numeric + default 0 if missing
    normalized_scores: Dict[str, int] = {}
    for key in ["aptitude", "listening", "reading"]:
        val = scores.get(key, 0)
        try:
            normalized_scores[key] = int(val)
        except (TypeError, ValueError):
            normalized_scores[key] = 0

    if not normalized_scores:
        # No scores yet
        performance_html = """
        <div style='background:white;padding:3rem;border-radius:20px;
                    box-shadow:0 10px 40px rgba(0,0,0,0.08);text-align:center;'>
            <div style='font-size:4rem;margin-bottom:1rem;'>📊</div>
            <h3 style='color:#6b7280;margin:0;font-size:1.5rem;'>No test data available</h3>
            <p style='color:#9ca3af;margin:0.5rem 0 0 0;'>Complete a test to see your results</p>
        </div>
        """
        return performance_html, "", ""

    # Use utility scoring function for overall stats
    final = calculate_final_score(normalized_scores)
    total_score = final["total_score"]
    max_score = final["max_score"]
    percentage = round(final["percentage"], 1)
    performance_level = final["performance_level"]

    # Determine performance styling
    if percentage >= 80:
        perf_gradient = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
        perf_emoji = "🌟"
        perf_message = "Outstanding Performance!"
    elif percentage >= 60:
        perf_gradient = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
        perf_emoji = "👍"
        perf_message = "Good Performance!"
    else:
        perf_gradient = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
        perf_emoji = "💪"
        perf_message = "Keep Practicing!"

    detailed_feedback_html = _generate_detailed_feedback(normalized_scores)
    personalized_tips = _generate_personalized_tips(normalized_scores, percentage)
    study_plan = _generate_study_plan(percentage, normalized_scores)

    # ----- Overall Score Card -----
    performance_html = f"""
        <style>
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-10px); }}
            }}
            .float-animation {{
                animation: float 3s ease-in-out infinite;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.95); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}
            .fade-in {{
                animation: fadeIn 0.5s ease-out;
            }}
        </style>
        
        <div style='background:{perf_gradient};padding:3rem 2rem;border-radius:20px;
                    text-align:center;margin-bottom:2rem;color:white;
                    box-shadow:0 20px 60px rgba(0,0,0,0.2);position:relative;overflow:hidden;' 
             class='fade-in'>
            <div style='position:absolute;top:-50px;right:-50px;font-size:20rem;opacity:0.1;' 
                 class='float-animation'>{perf_emoji}</div>
            <div style='position:relative;z-index:1;'>
                <div style='font-size:4rem;margin-bottom:0.5rem;' class='float-animation'>{perf_emoji}</div>
                <h1 style='color:white;margin:0 0 0.5rem 0;font-size:2.5rem;font-weight:800;'>
                    {perf_message}
                </h1>
                <div style='font-size:1.1rem;opacity:0.9;margin-bottom:2rem;'>
                    Comprehensive Test Results
                </div>
                
                <div style='background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);
                            padding:2rem;border-radius:16px;border:2px solid rgba(255,255,255,0.3);
                            max-width:500px;margin:0 auto;'>
                    <div style='font-size:1rem;opacity:0.95;margin-bottom:1rem;
                                text-transform:uppercase;letter-spacing:2px;font-weight:600;'>
                        Your Total Score
                    </div>
                    <div style='font-size:6rem;font-weight:900;line-height:1;
                                text-shadow:0 4px 10px rgba(0,0,0,0.2);margin:1rem 0;'>
                        {total_score}<span style='font-size:3rem;opacity:0.8;'>/{max_score}</span>
                    </div>
                    <div style='font-size:2.5rem;font-weight:700;opacity:0.95;margin-bottom:0.5rem;'>
                        {percentage}%
                    </div>
                    <div style='background:rgba(255,255,255,0.9);color:#1a1a1a;
                                padding:0.75rem 1.5rem;border-radius:25px;
                                font-size:1.2rem;font-weight:700;display:inline-block;
                                box-shadow:0 4px 15px rgba(0,0,0,0.1);'>
                        {performance_level}
                    </div>
                </div>
            </div>
        </div>
        
        <div style='background:white;padding:2.5rem;border-radius:20px;
                    box-shadow:0 10px 40px rgba(0,0,0,0.08);' class='fade-in'>
            <div style='text-align:center;margin-bottom:2rem;'>
                <h2 style='color:#1a1a1a;margin:0;font-size:2rem;font-weight:700;'>
                    📊 Section Breakdown
                </h2>
                <p style='color:#6b7280;margin:0.5rem 0 0 0;font-size:1rem;'>
                    Detailed performance analysis for each section
                </p>
            </div>
            
            {detailed_feedback_html}
        </div>
    """

    # ----- Tips Card -----
    tips_html_parts = []
    tip_icons = {
        "Aptitude": "🧮",
        "Listening": "🎧",
        "Reading": "📖"
    }
    tip_colors = {
        "Aptitude": "#8b5cf6",
        "Listening": "#3b82f6",
        "Reading": "#f59e0b"
    }
    
    for area, tip in personalized_tips.items():
        color = tip_colors.get(area, "#667eea")
        icon = tip_icons.get(area, "💡")
        tips_html_parts.append(f"""
            <div style='background:linear-gradient(135deg, {color}15 0%, {color}25 100%);
                        padding:1.5rem;border-radius:12px;margin-bottom:1rem;
                        border-left:5px solid {color};box-shadow:0 4px 15px rgba(0,0,0,0.06);'>
                <div style='display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;'>
                    <span style='font-size:2rem;'>{icon}</span>
                    <strong style='color:#1a1a1a;font-size:1.2rem;'>{area}</strong>
                </div>
                <div style='color:#374151;font-size:1rem;line-height:1.7;margin-left:2.75rem;'>
                    {tip}
                </div>
            </div>
        """)

    tips_html = f"""
        <div style='background:white;padding:2.5rem;border-radius:20px;
                    box-shadow:0 10px 40px rgba(0,0,0,0.08);' class='fade-in'>
            <div style='text-align:center;margin-bottom:2rem;'>
                <h2 style='color:#1a1a1a;margin:0;font-size:2rem;font-weight:700;'>
                    💡 Personalized Tips
                </h2>
                <p style='color:#6b7280;margin:0.5rem 0 0 0;font-size:1rem;'>
                    Tailored recommendations to improve your skills
                </p>
            </div>
            
            {''.join(tips_html_parts)}
        </div>
    """

    # ----- Study Plan Card -----
    plan_icons = {
        "Daily Practice": "📅",
        "Weekly Schedule": "📆",
        "Key Focus": "🎯",
        "Practice Tests": "📝"
    }
    
    plan_html_parts = []
    for aspect, recommendation in study_plan.items():
        icon = plan_icons.get(aspect, "✓")
        plan_html_parts.append(f"""
            <div style='display:flex;gap:1rem;padding:1.25rem;
                        background:#f9fafb;border-radius:12px;margin-bottom:1rem;
                        border:2px solid #e5e7eb;transition:all 0.3s ease;'>
                <div style='font-size:2rem;line-height:1;flex-shrink:0;'>{icon}</div>
                <div style='flex:1;'>
                    <div style='color:#1a1a1a;font-weight:700;font-size:1.1rem;margin-bottom:0.5rem;'>
                        {aspect}
                    </div>
                    <div style='color:#4b5563;font-size:1rem;line-height:1.6;'>
                        {recommendation}
                    </div>
                </div>
            </div>
        """)

    plan_html = f"""
        <div style='background:white;padding:2.5rem;border-radius:20px;
                    box-shadow:0 10px 40px rgba(0,0,0,0.08);' class='fade-in'>
            <div style='text-align:center;margin-bottom:2rem;'>
                <h2 style='color:#1a1a1a;margin:0;font-size:2rem;font-weight:700;'>
                    📚 Your Study Plan
                </h2>
                <p style='color:#6b7280;margin:0.5rem 0 0 0;font-size:1rem;'>
                    A customized roadmap based on your performance
                </p>
            </div>
            
            {''.join(plan_html_parts)}
            
            <div style='background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding:1.5rem;border-radius:12px;margin-top:1.5rem;text-align:center;
                        color:white;box-shadow:0 4px 15px rgba(102,126,234,0.3);'>
                <div style='font-size:1.5rem;margin-bottom:0.5rem;'>🎓</div>
                <div style='font-weight:600;font-size:1.1rem;'>
                    Consistency is key to success! Follow this plan and track your progress.
                </div>
            </div>
        </div>
    """

    return performance_html, tips_html, plan_html


def reset_results_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reset state to start a new test.
    You can customize this depending on how you manage global state.
    """
    # Minimal safe reset – keeps difficulty/name if you want
    state["current_page"] = "setup"
    state["scores"] = {"aptitude": 0, "listening": 0, "reading": 0}

    # Optionally clear per-round details if you track them:
    for key in [
        "aptitude_questions",
        "current_question",
        "aptitude_score",
        "answers",
        "listening_content",
        "listening_answers",
        "listening_score",
        "reading_content",
        "summary_text",
        "summary_submitted",
    ]:
        if key in state:
            state[key] = None if "score" not in key else 0

    return state


# ---------- Gradio UI construction ----------

def build_results_ui():
    """
    Build the Gradio components for the Results "page".

    Returns a dict of components so the main app can wire callbacks:
      {
        "grid": grid_html,
        "performance": performance_html,
        "tips": tips_html,
        "plan": plan_html,
        "restart_btn": restart_button,
      }
    """
    # Hero header
    hero = gr.HTML("""
        <div style='text-align:center;margin:3rem 0 2rem 0;'>
            <div style='font-size:5rem;margin-bottom:1rem;'>🏆</div>
            <h1 style='color:#1a1a1a;margin:0;font-size:3rem;font-weight:800;
                       background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                       background-clip:text;'>
                Test Results Dashboard
            </h1>
            <p style='color:#6b7280;font-size:1.2rem;margin:0.5rem 0 0 0;'>
                Comprehensive analysis of your performance
            </p>
        </div>
    """)

    with gr.Column() as grid:
        performance_html = gr.HTML()
        
        with gr.Row(equal_height=True):
            tips_html = gr.HTML()
            plan_html = gr.HTML()
        
        with gr.Row():
            restart_btn = gr.Button(
                "🔄 Start New Test",
                variant="primary",
                size="lg",
                scale=1
            )

    return {
        "hero": hero,
        "grid": grid,
        "performance": performance_html,
        "tips": tips_html,
        "plan": plan_html,
        "restart_btn": restart_btn,
    }


def update_results_view(state: Dict[str, Any]) -> tuple[Dict[str, Any], str, str, str]:
    """
    Hook function to plug into Gradio:
    - Takes the `state` dict
    - Returns updated state + HTML for 3 panels
    """
    perf_html, tips_html, plan_html = _render_results_html(state)
    return state, perf_html, tips_html, plan_html