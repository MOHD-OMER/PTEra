"""Main application file for PTE Mock Test - Professional Beautiful UI."""
import os
import sys
import gradio as gr
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.rounds.aptitude import (
    build_aptitude_ui, initialize_aptitude_round, 
    submit_aptitude_answer, clear_response
)
from src.rounds.listening import (
    build_listening_ui, initialize_listening, 
    update_listening, handle_listening_next
)
from src.rounds.reading import (
    build_reading_ui, initialize_reading_round, 
    update_reading_round, submit_summary, update_word_count
)
from src.utils.results import build_results_ui as build_results_dashboard, update_results_view
from src.auth.session import initialize_session_state, validate_state
from src.utils.timer import start_timer, get_remaining_time, format_time

# Professional Modern CSS with Premium Design System
PROFESSIONAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --primary: #2563eb;
    --primary-light: #3b82f6;
    --primary-dark: #1d4ed8;
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent: #8b5cf6;
    --accent-light: #a78bfa;
    --success: #10b981;
    --success-light: #34d399;
    --warning: #f59e0b;
    --danger: #ef4444;
    --dark: #0f172a;
    --dark-light: #1e293b;
    --gray: #64748b;
    --gray-light: #94a3b8;
    --gray-lighter: #cbd5e1;
    --bg: #f8fafc;
    --bg-secondary: #f1f5f9;
    --white: #ffffff;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    --radius: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

body, .gradio-container {
    background: var(--bg) !important;
    min-height: 100vh;
}

.gr-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 0 1.5rem !important;
}

/* Modern Glass Morphism Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: var(--shadow-md) !important;
    border-radius: var(--radius-lg) !important;
    transition: var(--transition) !important;
    padding: 2rem !important;
}

.glass-card:hover {
    box-shadow: var(--shadow-lg) !important;
    transform: translateY(-4px) !important;
}

/* Premium Hero Section */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 2rem;
    border-radius: var(--radius-xl);
    margin: 2rem 0;
    box-shadow: var(--shadow-xl);
    position: relative;
    overflow: hidden;
    text-align: center;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
        radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
    pointer-events: none;
}

.hero-section h1 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 4rem !important;
    font-weight: 900 !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    background: none !important;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    margin: 0 0 1rem 0 !important;
    letter-spacing: -0.03em !important;
}

.hero-subtitle {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.95) !important;
    margin: 0 0 1rem 0;
}

.hero-description {
    font-size: 1.125rem !important;
    color: rgba(255,255,255,0.85) !important;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.7;
    text-align: center;
}

/* Modern Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    color: var(--dark) !important;
    letter-spacing: -0.02em !important;
    -webkit-text-fill-color: var(--dark) !important;
    background: none !important;
}

h1 { font-size: 3rem !important; margin: 2rem 0 1rem 0 !important; }
h2 { font-size: 2.25rem !important; margin: 1.75rem 0 1rem 0 !important; }
h3 { font-size: 1.75rem !important; margin: 1.5rem 0 0.75rem 0 !important; }

.gr-button {
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 1rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: var(--dark) !important;
    background: white !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    transition: var(--transition) !important;
    text-transform: none !important;
    letter-spacing: 0.01em;
    position: relative;
    overflow: hidden;
    min-height: 56px;
}

.gr-button-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4) !important;
}

.gr-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.gr-button:hover::before {
    left: 100%;
}

.gr-button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
}

.gr-button:active {
    transform: translateY(0) scale(0.98) !important;
}

.gr-button-secondary {
    background: white !important;
    color: var(--primary) !important;
    border: 2px solid var(--primary) !important;
    box-shadow: var(--shadow-sm) !important;
}

.gr-button-secondary:hover {
    background: var(--primary) !important;
    color: white !important;
    box-shadow: var(--shadow-md) !important;
}

/* Professional Navigation Bar */
.navbar {
    background: white !important;
    backdrop-filter: blur(20px);
    padding: 1rem;
    border-radius: var(--radius-lg);
    margin: 1.5rem 0;
    box-shadow: var(--shadow-md) !important;
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
    border: 1px solid rgba(0,0,0,0.05);
}

.navbar button {
    padding: 0.875rem 1.75rem !important;
    font-size: 0.95rem !important;
    border-radius: var(--radius) !important;
    min-height: 52px;
    flex: 1;
    max-width: 160px;
    font-weight: 600 !important;
}

/* Modern Tab System - Hide Navigation */
.gr-tabs {
    background: transparent !important;
    border: none !important;
}

/* Scoped tab header hiding to main tabs only */
#pte-main-tabs > div:first-child {
    display: none !important;
}

/* Premium Form Inputs */
input, textarea, select, .gr-input, .gr-text-input, .gr-dropdown {
    background: white !important;
    border: 2px solid var(--gray-lighter) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.25rem !important;
    font-size: 1rem !important;
    color: var(--dark) !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-sm) !important;
}

input:focus, textarea:focus, select:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
    background: white !important;
}

/* Modern Radio Buttons */
.gr-radio {
    background: white !important;
    padding: 1.5rem !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
    border: 1px solid var(--gray-lighter) !important;
}

.gr-radio label {
    padding: 1rem 1.5rem !important;
    border-radius: var(--radius) !important;
    transition: var(--transition) !important;
    cursor: pointer !important;
    background: var(--bg) !important;
    margin: 0.5rem 0 !important;
    border: 2px solid transparent !important;
    font-weight: 500 !important;
}

.gr-radio label:hover {
    background: rgba(102, 126, 234, 0.05) !important;
    border-color: var(--primary-light) !important;
    transform: translateX(4px) !important;
}

/* Premium Progress System */
.progress-container {
    background: white;
    padding: 1.5rem;
    border-radius: var(--radius);
    margin: 1.5rem 0;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--gray-lighter);
}

.progress-bar {
    height: 10px;
    background: var(--bg-secondary);
    border-radius: 5px;
    overflow: hidden;
    position: relative;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
    border-radius: 5px;
    transition: width 0.4s ease;
    position: relative;
}

.progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Premium Timer Badge */
.timer-badge {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    padding: 1rem 2rem;
    border-radius: var(--radius);
    font-size: 1.5rem;
    font-weight: 700;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
    display: inline-block;
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: 0.05em;
}

.timer-badge.warning {
    animation: pulse-warning 1.5s infinite;
}

@keyframes pulse-warning {
    0%, 100% {
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
        transform: scale(1);
    }
    50% {
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.6);
        transform: scale(1.05);
    }
}

/* Premium Score Card */
.score-card {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 3rem;
    border-radius: var(--radius-xl);
    text-align: center;
    box-shadow: var(--shadow-xl);
    position: relative;
    overflow: hidden;
}

.score-card::before {
    content: '';
    position: absolute;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    top: -50px;
    right: -50px;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

.score-number {
    font-size: 4rem;
    font-weight: 900;
    font-family: 'Outfit', sans-serif !important;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    position: relative;
    z-index: 1;
}

/* Modern Question Card */
.question-card {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    margin: 1.5rem 0;
    box-shadow: var(--shadow-md);
    border-left: 4px solid var(--primary);
    transition: var(--transition);
    position: relative;
}

.question-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateX(4px);
}

/* Premium Badge System */
.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius);
    font-size: 0.95rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    box-shadow: var(--shadow-sm);
    gap: 0.5rem;
}

.badge-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.badge-success {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
}

.badge-danger {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
}

.badge-info {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
}

/* Feature Cards */
.feature-card {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    transition: var(--transition);
    border: 1px solid var(--gray-lighter);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.stat-card {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    text-align: center;
    transition: var(--transition);
    border-top: 4px solid var(--primary);
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 900;
    font-family: 'Outfit', sans-serif !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 0.95rem;
    color: var(--gray);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.5rem;
}

/* Messages */
.error-message {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    color: var(--dark);
    padding: 1.25rem 1.5rem;
    border-radius: var(--radius);
    margin: 1.5rem 0;
    box-shadow: var(--shadow-sm);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 1rem;
    border-left: 4px solid var(--danger);
}

.success-message {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    color: var(--dark);
    padding: 1.25rem 1.5rem;
    border-radius: var(--radius);
    margin: 1.5rem 0;
    box-shadow: var(--shadow-sm);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 1rem;
    border-left: 4px solid var(--success);
}

/* Footer */
.footer {
    background: white;
    backdrop-filter: blur(20px);
    padding: 3rem 2rem;
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
    margin-top: 4rem;
    text-align: center;
    box-shadow: var(--shadow-lg);
    border-top: 1px solid var(--gray-lighter);
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.footer-links a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
    transition: var(--transition);
    font-size: 0.95rem;
}

.footer-links a:hover {
    color: var(--accent);
    transform: translateY(-2px);
}

.social-icons {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.social-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    border-radius: 50%;
    font-size: 1.5rem;
    transition: var(--transition);
    cursor: pointer;
    box-shadow: var(--shadow-sm);
}

.social-icon:hover {
    transform: translateY(-4px) scale(1.1);
    box-shadow: var(--shadow-md);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.footer-copyright {
    color: var(--dark) !important;
    font-size: 0.9rem;
    font-weight: 500;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.slide-in {
    animation: slideInRight 0.6s ease-out;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-section h1 { font-size: 2.5rem !important; }
    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.75rem !important; }
    h3 { font-size: 1.5rem !important; }
   
    .hero-section {
        padding: 3rem 1.5rem;
    }
   
    button {
        padding: 0.875rem 1.5rem !important;
        font-size: 0.95rem !important;
    }
   
    .score-number {
        font-size: 3rem;
    }
   
    .navbar {
        gap: 0.5rem;
        padding: 0.75rem;
    }

    .navbar button {
        max-width: none;
        min-width: 140px;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }
}

/* Utility Classes */
.text-center { text-align: center !important; }
.text-primary { color: var(--primary) !important; }
.text-gray { color: var(--gray) !important; }
.mb-2 { margin-bottom: 1rem !important; }
.mb-4 { margin-bottom: 2rem !important; }
.mt-4 { margin-top: 2rem !important; }

.emoji {
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", sans-serif !important;
    font-size: 1.25em;
    line-height: 1;
    display: inline-block;
    margin-right: 0.25em;
    background: none !important;
    -webkit-background-clip: initial !important;
    -webkit-text-fill-color: initial !important;
    background-clip: initial !important;
    color: var(--dark) !important;
}
"""

def _update_nav_state(section):
    """Return updates for navigation state."""
    is_setup = section == "setup"
    is_test = section in ["aptitude", "listening", "reading"]
    is_results = section == "results"
    is_about = section == "about"
    
    return [
        gr.update(selected=section),
        gr.update(value="", visible=True),
        gr.update(variant="primary" if is_setup else "secondary"),
        gr.update(variant="primary" if is_test else "secondary"),
        gr.update(variant="primary" if is_about else "secondary"),
        gr.update(variant="primary" if is_results else "secondary")
    ]

def start_test(user_name, difficulty, state):
    """Initialize test with user configuration."""
    if not user_name or not user_name.strip():
        base_updates = _update_nav_state("setup")
        base_updates[1] = gr.update(value="⚠️ **Error:** Please enter your name to continue.", visible=True)
        return (state, gr.update(value=user_name), gr.update(value=difficulty), *base_updates)
    
    if not difficulty:
        base_updates = _update_nav_state("setup")
        base_updates[1] = gr.update(value="⚠️ **Error:** Please select a difficulty level.", visible=True)
        return (state, gr.update(value=user_name), gr.update(value=difficulty), *base_updates)
    
    new_state = initialize_session_state()
    new_state['user_name'] = user_name.strip()
    new_state['difficulty'] = difficulty
    new_state['test_start_time'] = datetime.now().isoformat()
    new_state['current_page'] = 'aptitude'
    new_state['scores'] = {}
    
    start_timer(new_state, 720)
    nav_updates = _update_nav_state("aptitude")
    
    return (new_state, gr.update(value=""), gr.update(value=None), *nav_updates)

def navigate_to_listening(state):
    """Navigate from aptitude to listening."""
    new_state = state.copy() if isinstance(state, dict) else {}
    new_state['current_page'] = 'listening'
    start_timer(new_state, 180)
    nav_updates = _update_nav_state("listening")
    return (new_state, *nav_updates)

def navigate_to_reading(state):
    """Navigate from listening to reading."""
    new_state = state.copy() if isinstance(state, dict) else {}
    new_state['current_page'] = 'reading'
    start_timer(new_state, 300)
    nav_updates = _update_nav_state("reading")
    return (new_state, gr.update(active=True), *nav_updates)

def navigate_to_results(state):
    """Navigate from reading to results."""
    new_state = state.copy() if isinstance(state, dict) else {}
    new_state['current_page'] = 'results'
    new_state['test_end_time'] = datetime.now().isoformat()
    nav_updates = _update_nav_state("results")
    return (new_state, gr.update(active=False), *nav_updates)

def restart_test(state):
    """Reset the test and return to setup page."""
    new_state = initialize_session_state()
    nav_updates = _update_nav_state("setup")
    return (new_state, *nav_updates)

def show_home(state):
    """Show home/setup page."""
    nav_updates = _update_nav_state("setup")
    return (state, *nav_updates)

def show_about(state):
    """Show about page."""
    nav_updates = _update_nav_state("about")
    return (state, *nav_updates)

def show_test_section(state):
    """Show the current test round."""
    current = state.get("current_page", "setup") if isinstance(state, dict) else "setup"
    if current not in {"aptitude", "listening", "reading", "results"}:
        current = "setup"
    nav_updates = _update_nav_state(current)
    return (state, *nav_updates)

def show_results_section(state):
    """Show results page."""
    nav_updates = _update_nav_state("results")
    return (state, *nav_updates)

def build_about_ui():
    """Create About page with professional styling."""
    with gr.Column() as about_container:
        gr.HTML("""
            <div class="hero-section">
                <h1><span class="emoji">🎓</span>About PTEra</h1>
                <p class="hero-subtitle">Professional PTE Academic Assessment Platform</p>
                <p class="hero-description" style="text-align:center; margin: 0 auto;">
                    Experience comprehensive test preparation with real-time scoring, adaptive difficulty,
                    and expert-designed assessment modules
                </p>
            </div>
        """)
        
        gr.HTML("""
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">3</div>
                    <div class="stat-label" style="color: black;">Test Modules</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">25</div>
                    <div class="stat-label" style="color: black;">Total Minutes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">100%</div>
                    <div class="stat-label" style="color: black;">Accurate Scoring</div>
                </div>
            </div>
        """)
        
        gr.HTML("""
            <div class="glass-card" style="margin: 2rem 0;">
                <h2 class="text-center"><span class="emoji">✨</span> Premium Features</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
                    <div class="feature-card">
                        <span class="feature-icon emoji">🎯</span>
                        <h4 style="margin: 0.5rem 0; color: var(--dark);">Comprehensive Testing</h4>
                        <p style="color: var(--gray); margin: 0;">Three complete assessment modules covering aptitude, listening, and reading comprehension.</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon emoji">⏱️</span>
                        <h4 style="margin: 0.5rem 0; color: var(--dark);">Real-Time Timing</h4>
                        <p style="color: var(--gray); margin: 0;">Strict timed sections with automatic progression to simulate exam conditions.</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon emoji">📊</span>
                        <h4 style="margin: 0.5rem 0; color: var(--dark);">Instant Analytics</h4>
                        <p style="color: var(--gray); margin: 0;">Detailed performance breakdown and personalized improvement recommendations.</p>
                    </div>
                </div>
            </div>
        """)
        
        gr.HTML("""
            <div class="glass-card" style="margin: 2rem 0;">
                <h2 class="text-center"><span class="emoji">🚀</span> How It Works</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
                    <div class="feature-card slide-in">
                        <span class="feature-icon emoji">1️⃣</span>
                        <h4 style="margin: 0.5rem 0; color: var(--dark);">Setup & Start</h4>
                        <p style="color: var(--gray); margin: 0;">Enter your details, select difficulty, and begin your assessment journey.</p>
                    </div>
                    <div class="feature-card slide-in">
                        <span class="feature-icon emoji">2️⃣</span>
                        <h4 style="margin: 0.5rem 0; color: var(--dark);">Complete Modules</h4>
                        <p style="color: var(--gray); margin: 0;">Progress through timed sections with interactive questions and audio elements.</p>
                    </div>
                    <div class="feature-card slide-in">
                        <span class="feature-icon emoji">3️⃣</span>
                        <h4 style="margin: 0.5rem 0; color: var(--dark);">Review & Improve</h4>
                        <p style="color: var(--gray); margin: 0;">Receive comprehensive results with actionable insights for better performance.</p>
                    </div>
                </div>
            </div>
        """)
    return about_container

def main():
    """Main application entry point with improved UI structure (no color/functionality changes)."""
    app = gr.Blocks(title="PTEra Mock Assessment")
    
    with app:
        # Inject CSS
        gr.HTML(f"<style>{PROFESSIONAL_CSS}</style>")

        # Initialize session state
        initial_state = initialize_session_state()
        if not validate_state(initial_state):
            initial_state = initialize_session_state()
        
        state = gr.State(initial_state)
        error_display = gr.Markdown(value="", visible=True)

        # --------------------------- NAVIGATION BAR ---------------------------
        with gr.Row(elem_classes="navbar"):
            home_btn     = gr.Button("🏠 Home",     variant="primary",   size="lg")
            test_btn     = gr.Button("📝 Test",     variant="secondary", size="lg")
            results_btn  = gr.Button("📊 Results",  variant="secondary", size="lg")
            about_btn    = gr.Button("ℹ️ About",    variant="secondary", size="lg")
        
        # --------------------------- MAIN TABS WRAPPER ---------------------------
        with gr.Tabs(elem_id="pte-main-tabs", elem_classes="main-tabs", selected="setup") as main_tabs:

            # --------------------------- SETUP TAB ---------------------------
            with gr.TabItem("Setup", id="setup"):
                with gr.Column(elem_classes="fade-in"):

                    # Hero Section
                    gr.HTML("""
                        <div class="hero-section">
                            <h1><span class="emoji">🎓</span> PTEra</h1>
                            <p class="hero-subtitle">Master Your PTE Academic Success</p>
                            <p class="hero-description" style="text-align:center; margin: 0 auto;">
                                Comprehensive Mock Test • Real-Time Scoring • Expert Feedback
                            </p>
                        </div>
                    """)

                    # Three Round Cards
                    gr.HTML("""
                        <div class="glass-card" style="padding: 2rem; margin: 2rem auto; max-width: 1100px;">
                            <h2 class="text-center"><span class="emoji">🎯</span> Three Comprehensive Test Rounds</h2>

                            <div style="
                                display: flex;
                                gap: 1.5rem;
                                margin: 1.5rem 0;
                                justify-content: center;
                                align-items: stretch;
                                flex-wrap: nowrap;
                            ">
                                <div class="badge-primary badge" style="padding: 1.5rem; font-size: 1rem;">
                                    <span class="emoji">📚</span>
                                    <div>Aptitude</div>
                                    <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.75rem;">12 minutes</div>
                                </div>

                                <div class="badge-success badge" style="padding: 1.5rem; font-size: 1rem;">
                                    <span class="emoji">🎧</span>
                                    <div>Listening</div>
                                    <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.75rem;">3 minutes</div>
                                </div>

                                <div class="badge-info badge" style="padding: 1.5rem; font-size: 1rem;">
                                    <span class="emoji">📖</span>
                                    <div>Reading</div>
                                    <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.75rem;">10 minutes</div>
                                </div>
                            </div>
                        </div>

                    """)

                    # Setup Form
                    with gr.Column(elem_classes="glass-card", elem_id="setup-form"):
                        gr.HTML('<h2 class="text-center"><span class="emoji">📋</span> Enter Your Details</h2>')
                        
                        user_name_input = gr.Textbox(
                            label="Full Name",
                            placeholder="Enter your full name...",
                            max_lines=1,
                            elem_classes="fade-in"
                        )
                        difficulty_selector = gr.Dropdown(
                            label="Difficulty Level",
                            choices=["Easy", "Medium", "Hard"],
                            value="Easy",
                            elem_classes="fade-in"
                        )
                        start_btn = gr.Button(
                            "🚀 Start Assessment Now",
                            variant="primary",
                            size="lg",
                            elem_classes="fade-in"
                        )

                    # Bottom Message
                    gr.HTML("""
                        <div style="text-align: center; margin: 3rem 0; padding: 2rem;
                                    background: rgba(102, 126, 234, 0.05);
                                    border-radius: 16px; border: 1px solid var(--gray-lighter);">
                            <p style="color: var(--primary); font-size: 1.125rem; font-weight: 600; margin: 0;">
                                Ready to begin your journey to success? <span class="emoji">🌟</span>
                            </p>
                        </div>
                    """)

            # --------------------------- OTHER TABS ---------------------------
            with gr.TabItem("Aptitude", id="aptitude"):
                aptitude_components = build_aptitude_ui()
            
            with gr.TabItem("Listening", id="listening"):
                listening_components = build_listening_ui()
            
            with gr.TabItem("Reading", id="reading"):
                reading_components = build_reading_ui()
            
            with gr.TabItem("About", id="about"):
                about_ui = build_about_ui()

            with gr.TabItem("Results", id="results"):
                results_components = build_results_dashboard()

        # --------------------------- FOOTER ---------------------------
        gr.HTML("""
            <div class="footer">
                <div class="footer-links">
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                    <a href="#">Contact Us</a>
                </div>
                <div class="social-icons">
                    <span class="social-icon emoji">📧</span>
                    <span class="social-icon emoji">🐦</span>
                    <span class="social-icon emoji">💼</span>
                </div>
                <div class="footer-copyright">
                    &copy; 2025 PTEra Mock Assessment. All rights reserved.
                </div>
            </div>
        """)

        # --------------------------- TARGETS & TIMER ---------------------------
        nav_targets = [main_tabs, error_display, home_btn, test_btn, about_btn, results_btn]
        timer = gr.Timer(1, active=False)

        # --------------------------- EVENT HANDLERS (UNCHANGED) ---------------------------

        setup_components = {
            'start_btn': start_btn,
            'user_name_input': user_name_input,
            'difficulty_selector': difficulty_selector
        }

        setup_components['start_btn'].click(
            fn=start_test,
            inputs=[user_name_input, difficulty_selector, state],
            outputs=[state, user_name_input, difficulty_selector, *nav_targets]
        ).then(
            fn=initialize_aptitude_round,
            inputs=[state],
            outputs=[
                state,
                aptitude_components['header'], aptitude_components['question_html'],
                aptitude_components['options'], aptitude_components['next_btn'],
                aptitude_components['continue_btn']
            ]
        )

        aptitude_components['clear_btn'].click(
            fn=clear_response,
            outputs=[aptitude_components['options']]
        )

        aptitude_components['next_btn'].click(
            fn=submit_aptitude_answer,
            inputs=[state, aptitude_components['options']],
            outputs=[
                state,
                aptitude_components['header'], aptitude_components['question_html'],
                aptitude_components['options'], aptitude_components['next_btn'],
                aptitude_components['continue_btn']
            ]
        )

        aptitude_components['continue_btn'].click(
            fn=navigate_to_listening, inputs=[state], outputs=[state, *nav_targets]
        ).then(
            fn=initialize_listening,
            inputs=[state],
            outputs=[
                state,
                listening_components['header'], listening_components['audio'],
                listening_components['passage_html'], listening_components['blanks_container'],
                listening_components['next_btn'], listening_components['continue_btn']
            ]
        )

        listening_components['next_btn'].click(
            fn=handle_listening_next,
            inputs=[state] + listening_components['blanks'],
            outputs=[
                state,
                listening_components['header'], listening_components['audio'],
                listening_components['passage_html'], listening_components['blanks_container'],
                listening_components['next_btn'], listening_components['continue_btn']
            ]
        )

        listening_components['continue_btn'].click(
            fn=navigate_to_reading, inputs=[state], outputs=[state, timer, *nav_targets]
        ).then(
            fn=initialize_reading_round,
            inputs=[state],
            outputs=[
                state,
                reading_components['header'], reading_components['passage_html'],
                reading_components['submit_btn'], reading_components['continue_btn']
            ]
        )

        timer.tick(
            fn=update_reading_round,
            inputs=[state],
            outputs=[
                state,
                reading_components['header'], reading_components['passage_html'],
                reading_components['submit_btn'], reading_components['continue_btn']
            ]
        )

        reading_components['submit_btn'].click(
            fn=submit_summary,
            inputs=[state] + reading_components['summary_input'],
            outputs=[
                state,
                reading_components['header'], reading_components['passage_html'],
                reading_components['submit_btn'], reading_components['continue_btn']
            ]
        )

        reading_components['continue_btn'].click(
            fn=navigate_to_results, inputs=[state], outputs=[state, timer, *nav_targets]
        ).then(
            fn=update_results_view,
            inputs=[state],
            outputs=[
                state,
                results_components["performance"],
                results_components["tips"],
                results_components["plan"]
            ]
        )

        results_components['restart_btn'].click(
            fn=restart_test, inputs=[state], outputs=[state, *nav_targets]
        )

        home_btn.click(fn=show_home, inputs=[state], outputs=[state, *nav_targets])
        test_btn.click(fn=show_test_section, inputs=[state], outputs=[state, *nav_targets])
        about_btn.click(fn=show_about, inputs=[state], outputs=[state, *nav_targets])
        results_btn.click(
            fn=show_results_section, inputs=[state], outputs=[state, *nav_targets]
        ).then(
            fn=update_results_view,
            inputs=[state],
            outputs=[
                state,
                results_components["performance"],
                results_components["tips"],
                results_components["plan"]
            ]
        )

    return app


if __name__ == "__main__":
    app = main()
    app.launch(server_name="0.0.0.0", server_port=7861, share=False)
