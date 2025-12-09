import gradio as gr
import time
from src.utils.aptitude_generation import generate_questions_multiround, MOCK_QUESTIONS
from src.utils.timer import get_remaining_time, format_time

# -------------------------------------------------------------------
# TIMER HELPERS (Integrated)
# -------------------------------------------------------------------
def get_remaining_time(state):
    if "aptitude_start" not in state:
        return 720.0
    elapsed = time.time() - state["aptitude_start"]
    return max(0.0, state.get("aptitude_limit", 720) - elapsed)

# -------------------------------------------------------------------
# INITIALIZE ROUND
# -------------------------------------------------------------------
def initialize_aptitude_round(state):
    """
    Initialize aptitude round - safely handle state initialization.
    Returns 6 values: (state, header, question, options, next_btn, continue_btn)
    """
    if not isinstance(state, dict):
        state = {}
    
    if "scores" not in state:
        state["scores"] = {}
    
    if not state.get("aptitude_questions"):
        try:
            difficulty = state.get("difficulty", "Easy")
            content = generate_questions_multiround(difficulty, num_questions=20)
            
            state["aptitude_questions"] = content["questions"]
            state["current_question"] = 0
            state["aptitude_score"] = 0
            state["answers"] = []
            state["aptitude_start"] = time.time()
            state["aptitude_limit"] = 720
            
        except Exception as e:
            state["aptitude_questions"] = MOCK_QUESTIONS[:20]
            state["current_question"] = 0
            state["aptitude_score"] = 0
            state["answers"] = []
            state["aptitude_start"] = time.time()
            state["aptitude_limit"] = 720
    
    return update_question(state)

# -------------------------------------------------------------------
# UPDATE QUESTION
# -------------------------------------------------------------------
def update_question(state):
    """
    Display current question or handle completion.
    Returns: (state, header_html, question_html, options_update, next_btn_update, continue_btn_update)
    """
    if "aptitude_questions" not in state or not state["aptitude_questions"]:
        question_html = """
            <div style='text-align: center; padding: 3rem; color: #64748b; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 24px; border: 2px dashed #cbd5e1;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>⏳</div>
                <p style='font-size: 1.125rem; font-weight: 500;'>Demo mode active - questions loading...</p>
            </div>
        """
        return (
            state,
            "",
            question_html,
            gr.update(choices=[], value=None, visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
        )
    
    questions = state["aptitude_questions"]
    current = state.get("current_question", 0)
    total = len(questions)

    if current >= total:
        return finish_aptitude_ui(state)

    remaining = get_remaining_time(state)
    if remaining <= 0:
        return time_up(state)

    q = questions[current]
    progress = (current + 1) / total
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    
    # Dynamic timer color based on urgency
    if remaining < 60:
        timer_color = "#ef4444"
        timer_bg = "#fee2e2"
        pulse_animation = "animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;"
    elif remaining < 180:
        timer_color = "#f59e0b"
        timer_bg = "#fef3c7"
        pulse_animation = ""
    else:
        timer_color = "#10b981"
        timer_bg = "#d1fae5"
        pulse_animation = ""

    header_html = f"""
        <style>
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateY(-10px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            .header-card {{
                animation: slideIn 0.4s ease-out;
            }}
        </style>
        <div class='header-card' style='background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); padding: 2rem; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04); margin-bottom: 2rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden;'>
            <div style='position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); opacity: 0.6;'></div>
            
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; gap: 2rem;'>
                <div style='flex: 1; text-align: left;'>
                    <div style='font-size: 0.8125rem; font-weight: 600; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;'>⏱️ Time Remaining</div>
                    <div style='display: inline-block; background: {timer_bg}; padding: 0.75rem 1.5rem; border-radius: 16px; border: 2px solid {timer_color}20; {pulse_animation}'>
                        <div style='font-size: 2.25rem; font-weight: 800; color: {timer_color}; font-family: "SF Mono", "Monaco", "Inconsolata", "Fira Code", "Droid Sans Mono", monospace; letter-spacing: -0.025em;'>{format_time(remaining)}</div>
                    </div>
                </div>
                
                <div style='flex: 1; text-align: right;'>
                    <div style='font-size: 0.8125rem; font-weight: 600; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;'>📊 Progress</div>
                    <div style='display: inline-block; background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); padding: 0.75rem 1.5rem; border-radius: 16px; border: 2px solid #3b82f620;'>
                        <div style='font-size: 1.5rem; font-weight: 700; color: #1e40af; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;'>
                            <span style='color: #3b82f6;'>{current+1}</span> <span style='color: #94a3b8; font-size: 1.25rem;'>/</span> <span style='color: #64748b;'>{total}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style='position: relative;'>
                <div style='height: 10px; background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); border-radius: 100px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);'>
                    <div style='width: {progress * 100}%; height: 100%; background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%); transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); border-radius: 100px; position: relative;'>
                        <div style='position: absolute; top: 0; right: 0; bottom: 0; width: 40%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3)); border-radius: 100px;'></div>
                    </div>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 0.5rem; padding: 0 0.25rem;'>
                    <span style='font-size: 0.75rem; font-weight: 500; color: #64748b;'>Question {current+1}</span>
                    <span style='font-size: 0.75rem; font-weight: 600; color: #3b82f6;'>{int(progress * 100)}% Complete</span>
                </div>
            </div>
        </div>
    """

    question_html = f"""
        <style>
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            .question-card {{
                animation: fadeInUp 0.5s ease-out;
            }}
        </style>
        <div class='question-card' style='background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%); padding: 3rem; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04); margin-bottom: 2rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden;'>
            <div style='position: absolute; top: 0; right: 0; width: 200px; height: 200px; background: radial-gradient(circle, rgba(139, 92, 246, 0.08) 0%, transparent 70%); pointer-events: none;'></div>
            
            <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;'>
                <div style='width: 48px; height: 48px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 16px; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3); flex-shrink: 0;'>
                    <span style='font-size: 1.5rem; font-weight: 700; color: white;'>Q{current+1}</span>
                </div>
                <div style='height: 2px; flex: 1; background: linear-gradient(90deg, #e2e8f0 0%, transparent 100%);'></div>
            </div>
            
            <div style='font-size: 1.25rem; color: #0f172a; line-height: 1.8; font-weight: 500; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; position: relative; z-index: 1;'>
                {q['question']}
            </div>
        </div>
    """

    return (
        state,
        header_html,
        question_html,
        gr.update(choices=q["options"], value=None, visible=True),
        gr.update(visible=True, interactive=True),
        gr.update(visible=False),
    )

def submit_aptitude_answer(state, selected_option):
    """Record answer and move to next question."""
    if not isinstance(state, dict):
        state = {}
    
    questions = state.get("aptitude_questions", [])
    current = state.get("current_question", 0)

    if current >= len(questions):
        return finish_aptitude_ui(state)

    q = questions[current]
    selected = selected_option or "Not answered"

    if selected == q.get("correct", ""):
        state["aptitude_score"] = state.get("aptitude_score", 0) + 1

    if "answers" not in state:
        state["answers"] = []
    
    state["answers"].append({
        "question": q["question"],
        "selected": selected,
        "correct": q.get("correct", ""),
        "explanation": q.get("explanation", "")
    })

    state["current_question"] = current + 1
    
    return update_question(state)

def clear_response():
    """Clear radio button selection."""
    return gr.update(value=None)

def time_up(state):
    """Handle forced submission when timer expires."""
    questions = state.get("aptitude_questions", [])
    current = state.get("current_question", 0)

    if current < len(questions):
        q = questions[current]
        
        if "answers" not in state:
            state["answers"] = []
            
        state["answers"].append({
            "question": q["question"],
            "selected": "Not answered",
            "correct": q.get("correct", ""),
            "explanation": q.get("explanation", "")
        })
        state["current_question"] = len(questions)

    return finish_aptitude_ui(state, time_up=True)

def finish_aptitude_ui(state, time_up=False):
    """Display completion screen with score."""
    raw = state.get("aptitude_score", 0)
    normalized = round((raw / 20) * 5)

    if "scores" not in state:
        state["scores"] = {}

    state["scores"]["aptitude"] = normalized
    state["current_page"] = "listening"

    msg = "⏰ Time's Up!" if time_up else "🎉 Excellent Work!"
    submsg = "Your answers have been automatically submitted." if time_up else "You've completed the aptitude assessment."
    
    # Dynamic gradient based on score
    if normalized >= 4:
        gradient = "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)"
        border_color = "#10b981"
        icon = "🌟"
    elif normalized >= 3:
        gradient = "linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)"
        border_color = "#3b82f6"
        icon = "✨"
    else:
        gradient = "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"
        border_color = "#f59e0b"
        icon = "💪"

    finish_html = f"""
        <style>
            @keyframes scaleIn {{
                from {{
                    opacity: 0;
                    transform: scale(0.9);
                }}
                to {{
                    opacity: 1;
                    transform: scale(1);
                }}
            }}
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-10px); }}
            }}
            .completion-card {{
                animation: scaleIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .score-badge {{
                animation: float 3s ease-in-out infinite;
            }}
        </style>
        <div class='completion-card' style='background: {gradient}; padding: 4rem 3rem; border: 3px solid {border_color}; border-radius: 32px; text-align: center; margin: 2rem 0; box-shadow: 0 20px 60px rgba(0,0,0,0.12), 0 8px 24px rgba(0,0,0,0.08); position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%); pointer-events: none;'></div>
            <div style='position: absolute; bottom: -30px; left: -30px; width: 150px; height: 150px; background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%); pointer-events: none;'></div>
            
            <div style='font-size: 4rem; margin-bottom: 1rem;'>{icon}</div>
            
            <h2 style='color: #0f172a; margin-bottom: 0.75rem; font-size: 2.25rem; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; letter-spacing: -0.025em;'>
                {msg}
            </h2>
            <p style='color: #475569; font-size: 1.125rem; font-weight: 400; margin-bottom: 2.5rem;'>{submsg}</p>
            
            <div class='score-badge' style='display: inline-block; background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); padding: 2.5rem 3.5rem; border-radius: 28px; box-shadow: 0 16px 48px rgba(0,0,0,0.15), inset 0 2px 4px rgba(255,255,255,0.8); border: 2px solid {border_color}40; margin-bottom: 2rem; position: relative;'>
                <div style='position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); border-radius: 28px 28px 0 0;'></div>
                
                <div style='font-size: 0.875rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;'>Your Score</div>
                <div style='font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1; letter-spacing: -0.02em;'>
                    {normalized}<span style='font-size: 3rem; opacity: 0.6;'>/5</span>
                </div>
            </div>
            
            <div style='background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); padding: 1.75rem 2rem; border-radius: 20px; margin: 2rem auto 2.5rem; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.8); max-width: 400px;'>
                <div style='display: flex; align-items: center; justify-content: center; gap: 1rem;'>
                    <div style='width: 48px; height: 48px; background: linear-gradient(135deg, {border_color}20, {border_color}30); border-radius: 12px; display: flex; align-items: center; justify-content: center;'>
                        <span style='font-size: 1.5rem;'>✓</span>
                    </div>
                    <div style='text-align: left;'>
                        <div style='font-size: 0.875rem; color: #64748b; font-weight: 500; margin-bottom: 0.25rem;'>Correct Answers</div>
                        <div style='font-size: 1.75rem; font-weight: 700; color: #0f172a;'>{raw} <span style='font-size: 1.125rem; color: #64748b; font-weight: 500;'>/ 20</span></div>
                    </div>
                </div>
            </div>
            
            <div style='background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(5px); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.6); max-width: 500px; margin: 0 auto;'>
                <p style='color: #475569; margin: 0; font-size: 1.0625rem; font-weight: 500; line-height: 1.6; display: flex; align-items: center; justify-content: center; gap: 0.5rem;'>
                    <span style='font-size: 1.5rem;'>🎧</span>
                    Ready for the Listening Round?
                </p>
            </div>
        </div>
    """

    return (
        state,
        "",
        finish_html,
        gr.update(choices=[], value=None, visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
    )

# -------------------------------------------------------------------
# UI BUILDER
# -------------------------------------------------------------------
def build_aptitude_ui():
    """Build the aptitude round UI components with beautiful, professional styling."""
    with gr.Column(scale=1, elem_classes=["professional-container"]):
        gr.HTML("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
                
                * {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                }
                
                .professional-container { 
                    max-width: 900px; 
                    margin: 0 auto; 
                    padding: 2.5rem 2rem; 
                }
                
                .professional-radio { 
                    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
                    border-radius: 20px; 
                    padding: 2rem; 
                    border: 2px solid #e2e8f0; 
                    box-shadow: 0 8px 24px rgba(0,0,0,0.06); 
                    transition: all 0.3s ease;
                }
                
                .professional-radio:hover {
                    box-shadow: 0 12px 32px rgba(0,0,0,0.1);
                    border-color: #cbd5e1;
                }
                
                .professional-radio label { 
                    font-size: 1.0625rem; 
                    color: #1e293b; 
                    font-weight: 500; 
                    padding: 1.125rem 1.5rem; 
                    border-radius: 14px; 
                    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); 
                    cursor: pointer; 
                    display: block; 
                    margin-bottom: 0.875rem; 
                    background: #fafbfc;
                    border: 2px solid #f1f5f9;
                    position: relative;
                    overflow: hidden;
                }
                
                .professional-radio label:hover { 
                    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); 
                    border-color: #cbd5e1;
                    transform: translateX(4px);
                }
                
                .professional-radio label::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 4px;
                    height: 100%;
                    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
                    opacity: 0;
                    transition: opacity 0.25s ease;
                }
                
                .professional-radio label:hover::before {
                    opacity: 0.3;
                }
                
                .professional-radio input:checked + label { 
                    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); 
                    color: white; 
                    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.35), 0 2px 8px rgba(139, 92, 246, 0.25); 
                    transform: translateX(4px) scale(1.02);
                    border-color: transparent;
                    font-weight: 600;
                }
                
                .professional-radio input:checked + label::before {
                    opacity: 1;
                    background: linear-gradient(180deg, rgba(255,255,255,0.3), rgba(255,255,255,0.1));
                    width: 100%;
                }
                
                .gr-button { 
                    border-radius: 14px; 
                    font-weight: 600; 
                    font-size: 1.0625rem; 
                    padding: 1rem 2rem; 
                    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); 
                    border: none; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    position: relative;
                    overflow: hidden;
                }
                
                .gr-button::before {
                    content: '';
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 0;
                    height: 0;
                    border-radius: 50%;
                    background: rgba(255,255,255,0.2);
                    transform: translate(-50%, -50%);
                    transition: width 0.6s ease, height 0.6s ease;
                }
                
                .gr-button:hover::before {
                    width: 300px;
                    height: 300px;
                }
                
                .gr-button:focus { 
                    outline: 3px solid #3b82f6; 
                    outline-offset: 3px; 
                }
                
                .gr-button:hover { 
                    transform: translateY(-2px); 
                    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                }
                
                .gr-button:active {
                    transform: translateY(0);
                }
                
                .gr-button.primary {
                    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                    color: white;
                }
                
                .gr-button.secondary {
                    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
                    color: #475569;
                }
                
                .clear-btn {
                    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
                    color: #92400e !important;
                    border: 2px solid #fbbf24 !important;
                }
                
                .next-btn {
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
                    color: white !important;
                }
                
                .continue-btn {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
                    color: white !important;
                    font-size: 1.125rem !important;
                    padding: 1.25rem 2.5rem !important;
                }
                
                h1 { 
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
                    font-weight: 800; 
                    letter-spacing: -0.04em; 
                }
            </style>
        """)
        
        title = gr.HTML("""
            <div style='text-align: center; margin: 3rem 0 3rem 0; position: relative;'>
                <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; height: 300px; background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%); pointer-events: none;'></div>
                <h1 style='font-size: 3.5rem; margin-bottom: 1rem; position: relative; z-index: 1;'>
                    <span style='display: inline-block; margin-right: 0.75rem; filter: drop-shadow(0 4px 8px rgba(59, 130, 246, 0.3));'>📝</span>
                    <span style='background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>
                        Aptitude Assessment
                    </span>
                </h1>
                <p style='font-size: 1.125rem; color: #64748b; font-weight: 500; margin: 0;'>Test your reasoning and analytical skills</p>
            </div>
        """)
        
        header = gr.HTML(value="")
        question_html = gr.HTML(value="")
        
        with gr.Group(elem_classes=["options-group"]):
            options = gr.Radio(
                label="💡 Select your answer:",
                choices=[],
                value=None,
                interactive=True,
                elem_classes=["professional-radio"]
            )

        answers_state = gr.State([])

        with gr.Row(variant="compact"):
            clear_btn = gr.Button("🔄 Clear Selection", variant="secondary", size="sm", elem_classes=["clear-btn"])
            next_btn = gr.Button("➡️ Next Question", variant="primary", visible=False, elem_classes=["next-btn"])
        
        continue_btn = gr.Button(
            "🎧 Continue to Listening Round →",
            visible=False,
            variant="primary",
            size="lg",
            elem_classes=["continue-btn"]
        )

    return {
        "title": title,
        "header": header,
        "question_html": question_html,
        "options": options,
        "answers": answers_state,
        "clear_btn": clear_btn,
        "next_btn": next_btn,
        "continue_btn": continue_btn,
    }