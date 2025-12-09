"""Listening Round with Beautiful Professional UI."""
import gradio as gr
import time
import os
import tempfile
from gtts import gTTS
from src.utils.listening_generation import generate_listening_content


def cleanup_audio(state):
    """Clean up temporary audio file."""
    path = state.get("audio_path")
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass
    state["audio_path"] = None
    return state


def create_audio_file(text: str) -> str:
    """Create temporary mp3 file using gTTS."""
    temp_dir = os.path.join(tempfile.gettempdir(), "pte_mock_audio")
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, f"listen_{int(time.time())}.mp3")
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(file_path)

    if not os.path.exists(file_path):
        raise RuntimeError("Audio generation failed")

    return file_path


def get_remaining_time(state):
    """Calculate remaining time for listening test."""
    if "listen_start" not in state:
        return 180.0  # 3 minutes
    elapsed = time.time() - state["listen_start"]
    return max(0.0, 180.0 - elapsed)


def initialize_listening(state):
    """Initialize the listening round with mixed questions."""
    if "scores" not in state:
        state["scores"] = {}
    
    if state.get("listening_content") is None:
        try:
            difficulty = state.get("difficulty", "Easy")
            content = generate_listening_content(difficulty)
            
            audio_path = create_audio_file(content["passage"])
            
            state["listening_content"] = content
            state["audio_path"] = audio_path
            state["listen_start"] = time.time()
            state["listening_submitted"] = False
            state["listening_answers"] = [None] * 5
            
        except Exception as e:
            error_html = f"""
                <div style='background:linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
                            border:2px solid #ef4444;padding:2.5rem;border-radius:16px;
                            box-shadow:0 10px 30px rgba(239,68,68,0.2);margin:3rem auto;max-width:600px;'>
                    <div style='text-align:center;'>
                        <div style='font-size:3rem;margin-bottom:1rem;'>⚠️</div>
                        <h3 style='color:#991b1b;margin:0 0 1rem 0;font-size:1.5rem;'>Content Generation Failed</h3>
                        <p style='color:#7f1d1d;font-size:1rem;margin:0;'>{str(e)}</p>
                    </div>
                </div>
            """
            return (state, error_html, None, "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False))
    
    return update_listening(state)


def update_listening(state):
    """Update UI with timer and current state."""
    remaining = get_remaining_time(state)
    
    if remaining <= 0 and not state.get("listening_submitted", False):
        return handle_listening_next(state, *state.get("listening_answers", [None]*5))
    
    content = state.get("listening_content")
    if not content:
        return initialize_listening(state)
    
    audio_path = state.get("audio_path")
    questions = content["questions"]
    
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    timer_color = "#ef4444" if remaining < 60 else "#4a6cf7"
    timer_bg = "#fee2e2" if remaining < 60 else "#eff6ff"
    
    header = f"""
        <style>
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
            .timer-warning {{
                animation: pulse 1.5s ease-in-out infinite;
            }}
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(-20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .slide-in {{
                animation: slideIn 0.5s ease-out;
            }}
        </style>
        
        <div style='background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding:2.5rem;border-radius:20px;margin-bottom:2rem;
                    box-shadow:0 20px 60px rgba(102,126,234,0.3);' class='slide-in'>
            <div style='text-align:center;color:white;margin-bottom:2rem;'>
                <div style='font-size:3rem;margin-bottom:0.5rem;'>🎧</div>
                <h1 style='color:white;margin:0;font-size:2.5rem;font-weight:700;'>Listening Round</h1>
            </div>
            
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:800px;margin:0 auto;'>
                <div style='background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);
                            padding:1.5rem;border-radius:16px;border:1px solid rgba(255,255,255,0.2);'>
                    <div style='font-size:0.9rem;color:rgba(255,255,255,0.9);margin-bottom:0.5rem;
                                text-transform:uppercase;letter-spacing:1px;font-weight:600;'>Time Remaining</div>
                    <div class='{"timer-warning" if remaining < 60 else ""}' 
                         style='font-size:3rem;font-weight:800;color:white;font-family:monospace;'>
                        {minutes:02d}:{seconds:02d}
                    </div>
                </div>
                
                <div style='background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);
                            padding:1.5rem;border-radius:16px;border:1px solid rgba(255,255,255,0.2);'>
                    <div style='font-size:0.9rem;color:rgba(255,255,255,0.9);margin-bottom:0.5rem;
                                text-transform:uppercase;letter-spacing:1px;font-weight:600;'>Topic</div>
                    <div style='font-size:1.4rem;font-weight:700;color:white;line-height:1.3;'>
                        {content.get('title', 'Listening Test')}
                    </div>
                </div>
            </div>
        </div>
        
        <div style='background:linear-gradient(to right, #fef3c7, #fde68a);
                    padding:1.5rem;border-left:5px solid #f59e0b;border-radius:12px;
                    margin-bottom:2rem;box-shadow:0 4px 15px rgba(245,158,11,0.2);'>
            <div style='display:flex;align-items:start;gap:1rem;'>
                <div style='font-size:2rem;line-height:1;'>📋</div>
                <div>
                    <div style='color:#78350f;font-weight:700;font-size:1.1rem;margin-bottom:0.5rem;'>
                        Instructions
                    </div>
                    <div style='color:#92400e;font-size:0.95rem;line-height:1.6;'>
                        Listen to the audio and answer all questions simultaneously below<br/>
                        <strong>• Fill in Blank:</strong> Type the exact word  
                        <strong>• True/False/Not Given:</strong> Type True, False, or Not Given
                    </div>
                </div>
            </div>
        </div>
    """
    
    type_styles = {
        "mcq": {
            "gradient": "linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)",
            "border": "#3b82f6",
            "badge_bg": "#1e40af",
            "badge_text": "#ffffff",
            "icon": "📝"
        },
        "fill_blank": {
            "gradient": "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)",
            "border": "#f59e0b",
            "badge_bg": "#92400e",
            "badge_text": "#ffffff",
            "icon": "✏️"
        },
        "true_false_not_given": {
            "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%)",
            "border": "#a855f7",
            "badge_bg": "#6b21a8",
            "badge_text": "#ffffff",
            "icon": "🔍"
        }
    }
    
    type_labels = {
        "mcq": "Multiple Choice",
        "fill_blank": "Fill in Blank",
        "true_false_not_given": "True/False/Not Given"
    }
    
    questions_html = "<div style='margin-top:1rem;'>"
    
    for i, q in enumerate(questions):
        style = type_styles.get(q["type"], type_styles["mcq"])
        type_label = type_labels.get(q["type"], "Question")
        
        questions_html += f"""
            <div style='background:{style["gradient"]};padding:1.75rem;border-radius:16px;
                        margin-bottom:1.25rem;border-left:5px solid {style["border"]};
                        box-shadow:0 4px 15px rgba(0,0,0,0.08);transition:transform 0.2s;'>
                <div style='display:flex;justify-content:space-between;align-items:start;gap:1rem;'>
                    <div style='flex:1;'>
                        <div style='display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;'>
                            <span style='font-size:1.8rem;line-height:1;'>{style["icon"]}</span>
                            <span style='background:{style["badge_bg"]};color:{style["badge_text"]};
                                         padding:0.4rem 0.9rem;border-radius:20px;font-size:0.75rem;
                                         font-weight:700;letter-spacing:0.5px;text-transform:uppercase;'>
                                {type_label}
                            </span>
                        </div>
                        <div style='font-weight:600;color:#1a1a1a;font-size:1.1rem;line-height:1.5;'>
                            <span style='color:{style["border"]};font-weight:800;'>Q{i+1}.</span> {q['question']}
                        </div>
                    </div>
                </div>
                <div style='margin-top:1rem;padding:0.75rem 1rem;background:rgba(255,255,255,0.7);
                            border-radius:8px;border:2px dashed {style["border"]};'>
                    <div style='color:#374151;font-size:0.9rem;font-weight:600;'>
                        ↓ Enter your answer in <span style='color:{style["border"]};'>Question {i+1} Answer</span> box below
                    </div>
                </div>
            </div>
        """
    
    questions_html += "</div>"
    
    return (
        state, header, audio_path, questions_html,
        gr.update(visible=True),
        gr.update(visible=True, value="Submit Answers →"), 
        gr.update(visible=False)
    )


def handle_listening_next(state, *answers):
    """Submit answers and show results."""
    content = state["listening_content"]
    questions = content["questions"]
    
    score = 0
    results = []
    
    for i, question in enumerate(questions):
        user_answer = answers[i] if i < len(answers) else None
        q_type = question["type"]
        correct_answer = question["correct_answer"]
        
        if q_type == "mcq":
            if user_answer in ["A", "B", "C", "D"]:
                user_idx = ["A", "B", "C", "D"].index(user_answer)
                is_correct = (user_idx == correct_answer)
            else:
                is_correct = False
        elif q_type == "fill_blank":
            user_text = str(user_answer).strip().lower() if user_answer else ""
            correct_text = str(correct_answer).strip().lower()
            is_correct = (user_text == correct_text)
        elif q_type == "true_false_not_given":
            is_correct = (user_answer == correct_answer)
        else:
            is_correct = False
        
        if is_correct:
            score += 1
        
        results.append({
            "type": q_type,
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "options": question.get("options", [])
        })
    
    state["listening_submitted"] = True
    state["scores"]["listening"] = score
    state["listening_results"] = results
    cleanup_audio(state)
    
    percentage = (score / 5) * 100
    
    # Determine performance level
    if percentage >= 80:
        performance_color = "#10b981"
        performance_text = "Excellent!"
        performance_emoji = "🌟"
    elif percentage >= 60:
        performance_color = "#f59e0b"
        performance_text = "Good Job!"
        performance_emoji = "👍"
    else:
        performance_color = "#ef4444"
        performance_text = "Keep Practicing!"
        performance_emoji = "💪"
    
    header = f"""
        <div style='background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding:3rem 2rem;border-radius:20px;text-align:center;
                    box-shadow:0 20px 60px rgba(102,126,234,0.3);margin-bottom:2rem;'>
            <div style='font-size:4rem;margin-bottom:1rem;'>🎉</div>
            <h1 style='color:white;margin:0;font-size:2.5rem;font-weight:700;'>
                Listening Round Complete!
            </h1>
        </div>
        
        <div style='background:linear-gradient(135deg, {performance_color} 0%, {performance_color}dd 100%);
                    padding:3rem;border-radius:20px;text-align:center;margin-bottom:2rem;
                    color:white;box-shadow:0 20px 60px rgba(0,0,0,0.15);position:relative;overflow:hidden;'>
            <div style='position:absolute;top:-50px;right:-50px;font-size:15rem;opacity:0.1;'>{performance_emoji}</div>
            <div style='position:relative;z-index:1;'>
                <div style='font-size:1.2rem;opacity:0.95;margin-bottom:1rem;font-weight:600;
                            text-transform:uppercase;letter-spacing:2px;'>Your Score</div>
                <div style='font-size:6rem;font-weight:900;margin:1rem 0;text-shadow:0 4px 10px rgba(0,0,0,0.2);'>
                    {score}<span style='font-size:3rem;opacity:0.8;'>/5</span>
                </div>
                <div style='font-size:2rem;opacity:0.95;font-weight:700;margin-bottom:0.5rem;'>{percentage:.0f}% Correct</div>
                <div style='font-size:1.5rem;opacity:0.9;font-weight:600;'>{performance_text}</div>
            </div>
        </div>
        
        <div style='background:white;padding:2.5rem;border-radius:20px;
                    box-shadow:0 10px 40px rgba(0,0,0,0.08);margin-top:2rem;'>
            <div style='text-align:center;margin-bottom:2rem;'>
                <h2 style='color:#1a1a1a;margin:0;font-size:2rem;font-weight:700;'>📝 Detailed Review</h2>
                <p style='color:#6b7280;margin:0.5rem 0 0 0;font-size:1rem;'>See how you performed on each question</p>
            </div>
    """
    
    for i, result in enumerate(results):
        if result["is_correct"]:
            icon = "✅"
            bg = "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)"
            border = "#10b981"
            status_badge = "Correct"
            status_color = "#065f46"
        else:
            icon = "❌"
            bg = "linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)"
            border = "#ef4444"
            status_badge = "Incorrect"
            status_color = "#991b1b"
        
        if result["type"] == "mcq":
            user_ans_text = result["user_answer"] if result["user_answer"] else "No answer provided"
            correct_ans_text = result["options"][result["correct_answer"]] if result["options"] else str(result["correct_answer"])
        elif result["type"] == "fill_blank":
            user_ans_text = result["user_answer"] if result["user_answer"] else "No answer provided"
            correct_ans_text = result["correct_answer"]
        else:
            user_ans_text = result["user_answer"] if result["user_answer"] else "No answer provided"
            correct_ans_text = result["correct_answer"]
        
        header += f"""
            <div style='background:{bg};border-left:6px solid {border};padding:2rem;
                        border-radius:16px;margin-bottom:1.5rem;box-shadow:0 4px 15px rgba(0,0,0,0.08);'>
                <div style='display:flex;justify-content:space-between;align-items:start;gap:1rem;margin-bottom:1rem;'>
                    <div style='display:flex;align-items:center;gap:0.75rem;'>
                        <span style='font-size:2rem;line-height:1;'>{icon}</span>
                        <span style='font-weight:700;color:#1a1a1a;font-size:1.2rem;'>Question {i+1}</span>
                    </div>
                    <span style='background:{status_color};color:white;padding:0.4rem 1rem;
                                 border-radius:20px;font-size:0.85rem;font-weight:700;'>
                        {status_badge}
                    </span>
                </div>
                
                <div style='color:#374151;font-size:1.05rem;margin-bottom:1.5rem;line-height:1.6;'>
                    {result["question"]}
                </div>
                
                <div style='background:rgba(255,255,255,0.7);padding:1.25rem;border-radius:12px;'>
                    <div style='margin-bottom:0.75rem;'>
                        <span style='color:#6b7280;font-weight:600;font-size:0.9rem;'>Your Answer:</span>
                        <div style='color:#1a1a1a;font-weight:600;font-size:1.05rem;margin-top:0.25rem;'>
                            {user_ans_text}
                        </div>
                    </div>
                    {f'''
                    <div style='border-top:2px dashed rgba(0,0,0,0.1);padding-top:0.75rem;margin-top:0.75rem;'>
                        <span style='color:#059669;font-weight:600;font-size:0.9rem;'>Correct Answer:</span>
                        <div style='color:#065f46;font-weight:700;font-size:1.05rem;margin-top:0.25rem;'>
                            {correct_ans_text}
                        </div>
                    </div>
                    ''' if not result["is_correct"] else ""}
                </div>
            </div>
        """
    
    header += """
        </div>
        
        <div style='text-align:center;margin:3rem 0 2rem 0;'>
            <p style='color:#6b7280;font-size:1.2rem;margin-bottom:1.5rem;font-weight:500;'>
                Ready to continue? Click below to proceed to the Reading round.
            </p>
        </div>
    """
    
    return (
        state, header, None, "",
        gr.update(visible=False),
        gr.update(visible=False), 
        gr.update(visible=True, value="Continue to Reading →")
    )


def build_listening_ui():
    """Build beautiful professional UI."""
    with gr.Column():
        title = gr.HTML("""
            <div style='text-align:center;margin:3rem 0 2rem 0;'>
                <div style='font-size:4rem;margin-bottom:1rem;'>🎧</div>
                <h1 style='color:#1a1a1a;margin:0;font-size:3rem;font-weight:800;
                           background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                           background-clip:text;'>
                    PTE Listening Test
                </h1>
                <p style='color:#6b7280;font-size:1.1rem;margin:0.5rem 0 0 0;'>
                    Professional English Listening Assessment
                </p>
            </div>
        """)
        
        header = gr.HTML()
        
        audio_player = gr.Audio(
            label="🔊 Audio Passage - Listen Carefully",
            interactive=False,
            visible=True,
            autoplay=True,
            show_label=True,
            container=True,
            elem_classes=["audio-player"]
        )
        
        passage_html = gr.HTML("", visible=True)
        
        with gr.Column(visible=False) as blanks_container:
            gr.HTML("""
                <div style='background:linear-gradient(to right, #eff6ff, #dbeafe);
                            padding:1.5rem;border-radius:12px;margin:1.5rem 0;
                            border-left:5px solid #3b82f6;'>
                    <h3 style='color:#1e40af;margin:0 0 0.5rem 0;font-size:1.3rem;font-weight:700;'>
                        📝 Your Answers
                    </h3>
                    <p style='color:#1e3a8a;margin:0;font-size:0.95rem;'>
                        Enter your answers below for each question
                    </p>
                </div>
            """)
            
            blanks = []
            for i in range(5):
                q_input = gr.Textbox(
                    label=f"Question {i+1} Answer",
                    placeholder="Type your answer here...",
                    lines=1,
                    container=True,
                    show_label=True
                )
                blanks.append(q_input)
        
        with gr.Row():
            next_btn = gr.Button(
                "Submit Answers →",
                variant="primary",
                visible=False,
                size="lg",
                scale=1
            )
            continue_btn = gr.Button(
                "Continue to Reading →",
                visible=False,
                variant="primary",
                size="lg",
                scale=1
            )
    
    return {
        "title": title, "header": header, "audio": audio_player,
        "passage_html": passage_html, "blanks_container": blanks_container,
        "blanks": blanks, "next_btn": next_btn, "continue_btn": continue_btn
    }