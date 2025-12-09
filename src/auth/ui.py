"""Enhanced UI components for authentication and user setup - Gradio version."""
import gradio as gr
from pathlib import Path
from datetime import datetime
import base64
import matplotlib.pyplot as plt
import numpy as np

def get_logo_base64():
    """Get or create the logo and return as base64."""
    current_dir = Path(__file__).parent.parent
    logo_path = current_dir / "static" / "logo.png"
    
    # Create default logo if it doesn't exist
    if not logo_path.exists():
        logo_path.parent.mkdir(exist_ok=True)
        
        plt.figure(figsize=(2, 2))
        plt.axis('off')
        
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        X, Y = np.meshgrid(x, y)
        plt.imshow(X + Y, cmap='RdPu', aspect='equal')
        
        plt.text(0.5, 0.5, 'PTE', 
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=28,
                fontweight='bold',
                color='white',
                fontfamily='sans-serif')
        
        plt.savefig(logo_path, bbox_inches='tight', pad_inches=0.03, dpi=100)
        plt.close()
    
    # Read and encode the logo
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_header_html():
    """Generate header HTML with embedded styles (Gradio-compatible)."""
    logo_base64 = get_logo_base64()
    
    css = """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary: #2563eb;
            --primary-light: #3b82f6;
            --secondary: #1e40af;
            --accent: #f59e0b;
            --success: #059669;
            --warning: #d97706;
            --error: #dc2626;
            --text-primary: #111827;
            --text-secondary: #374151;
            --text-muted: #6b7280;
            --background: #ffffff;
            --surface: #f8fafc;
            --surface-elevated: #ffffff;
            --border: #e5e7eb;
            --border-light: #f3f4f6;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        .welcome-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .welcome-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        }
        
        .welcome-header::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            padding: 0;
            position: relative;
            z-index: 2;
            flex-wrap: wrap;
        }
        
        .header-text h1 {
            color: #ffffff !important;
            margin: 0;
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            line-height: 1.2;
        }
        
        .welcome-subtitle-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.25rem;
        }
        
        .welcome-subtitle {
            color: rgba(255, 255, 255, 0.95) !important;
            margin: 0;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        }
        
        .welcome-subtitle-secondary {
            color: rgba(255, 255, 255, 0.85) !important;
            margin: 0;
            font-size: 0.85rem;
            font-weight: 400;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        }
        
        .header-logo {
            width: 50px;
            height: 50px;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .header-logo:hover {
            transform: scale(1.05);
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 0.75rem;
            }
            
            .header-text h1 {
                font-size: 1.25rem;
            }
            
            .welcome-subtitle {
                font-size: 0.9rem;
            }
            
            .welcome-subtitle-secondary {
                font-size: 0.8rem;
            }
            
            .welcome-header {
                padding: 1rem 0.75rem;
            }
            
            .header-logo {
                width: 45px;
                height: 45px;
            }
        }
    """
    
    html = f"""
        <style>{css}</style>
        <div class="welcome-header">
            <div class="header-content">
                <img src="data:image/png;base64,{logo_base64}" alt="PTE Logo" class="header-logo" width="50" height="50">
                <div class="header-text">
                    <h1>PTEra: Professional Mock Test</h1>
                    <div class="welcome-subtitle-container">
                        <p class="welcome-subtitle">Master Your PTE Academic Success</p>
                        <p class="welcome-subtitle-secondary">Comprehensive Assessment Platform for Excellence</p>
                    </div>
                </div>
            </div>
        </div>
    """
    
    return html

def get_test_structure_html():
    """Generate test structure HTML with embedded styles (Gradio-compatible)."""
    css = """
        .section-title {
            color: var(--text-primary) !important;
            font-size: 1.25rem;
            font-weight: 600;
            text-align: center;
            margin: 2rem 0 0.5rem 0;
            letter-spacing: -0.01em;
        }
        
        .section-subtitle {
            color: var(--text-secondary) !important;
            font-size: 0.9rem;
            text-align: center;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.5;
        }
        
        .round-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .round-card {
            background: var(--surface-elevated);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: left;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }
        
        .round-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            border-radius: 12px 12px 0 0;
        }
        
        .round-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.02) 0%, rgba(59, 130, 246, 0.02) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
            border-radius: 12px;
            pointer-events: none;
        }
        
        .round-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary);
        }
        
        .round-card:hover::after {
            opacity: 1;
        }
        
        .round-card .time {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
            letter-spacing: 0.02em;
            position: relative;
            top: -5px;
        }
        
        .round-card h3 {
            color: var(--text-primary) !important;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            letter-spacing: -0.01em;
            position: relative;
            padding-top: 0.25rem;
        }
        
        .round-card ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .round-card li {
            color: var(--text-secondary) !important;
            padding: 0.4rem 0 0.4rem 1.5rem;
            font-size: 0.85rem;
            line-height: 1.4;
            position: relative;
            font-weight: 400;
        }
        
        .round-card li::before {
            content: '✓';
            position: absolute;
            left: 0;
            top: 0.4rem;
            color: var(--success);
            font-weight: 700;
            font-size: 0.8rem;
        }
        
        @media (max-width: 768px) {
            .round-info {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .round-card {
                padding: 1.25rem;
            }
            
            .section-title {
                font-size: 1.1rem;
            }
            
            .section-subtitle {
                font-size: 0.85rem;
            }
        }
    """
    
    html = f"""
        <style>{css}</style>
        <div class="section-title">Comprehensive Test Structure</div>
        <p class="section-subtitle">Three expertly designed assessment rounds to evaluate your complete PTE readiness and academic potential</p>
        <div class="round-info">
            <div class="round-card">
                <div class="time">12 min</div>
                <h3>Aptitude & Reasoning</h3>
                <ul>
                    <li>20 dynamically generated aptitude questions</li>
                    <li>Advanced mathematical and logical reasoning</li>
                    <li>Adaptive difficulty based on performance</li>
                    <li>Detailed explanations for each solution</li>
                    <li>Comprehensive performance analytics</li>
                    <li>Personalized improvement roadmap</li>
                </ul>
            </div>
            <div class="round-card">
                <div class="time">3 min</div>
                <h3>Listening Comprehension</h3>
                <ul>
                    <li>5 carefully crafted listening comprehension questions</li>
                    <li>Advanced listening skills assessment</li>
                    <li>Adaptive difficulty based on performance</li>
                    <li>Real-time feedback and detailed scoring</li>
                    <li>Performance analytics and insights included</li>
                </ul>
            </div>
            <div class="round-card">
                <div class="time">5 min</div>
                <h3>Reading & Writing</h3>
                <ul>
                    <li>Structured summary writing assessment</li>
                    <li>Comprehensive language skills evaluation</li>
                    <li>Detailed feedback and improvement suggestions</li>
                </ul>
            </div>
        </div>
    """
    
    return html

def get_footer_html():
    """Generate footer HTML with embedded styles (Gradio-compatible)."""
    css = """
        .footer {
            margin-top: 2rem;
            padding: 1rem;
            text-align: center;
            background: var(--surface);
            border-top: 1px solid var(--border);
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            border-radius: 8px;
        }
        
        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
        }
        
        .footer-content {
            color: var(--text-secondary) !important;
            font-size: 0.8rem;
            margin: 0.75rem 0;
            font-weight: 400;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
        }
        
        .footer-link {
            color: var(--text-secondary) !important;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.25rem;
        }
        
        .footer-link:hover {
            color: var(--primary) !important;
        }
        
        .link-icon {
            font-size: 1.2rem;
            margin-bottom: 0.2rem;
        }
        
        @media (max-width: 768px) {
            .footer-links {
                gap: 1rem;
            }
            
            .footer-link {
                font-size: 0.75rem;
            }
            
            .link-icon {
                font-size: 1rem;
            }
        }
        
        @media (max-width: 480px) {
            .footer-links {
                gap: 0.75rem;
            }
        }
    """
    
    html = f"""
        <style>{css}</style>
        <div class="footer">
            <div class="footer-links">
                <a href="#" class="footer-link">
                    <span class="link-icon">📞</span>
                    <span>Support</span>
                </a>
                <a href="#" class="footer-link">
                    <span class="link-icon">🔒</span>
                    <span>Privacy</span>
                </a>
                <a href="#" class="footer-link">
                    <span class="link-icon">📋</span>
                    <span>Terms</span>
                </a>
                <a href="#" class="footer-link">
                    <span class="link-icon">📈</span>
                    <span>Analytics</span>
                </a>
            </div>
            <p class="footer-content">© 2025 PTEra Professional Mock Test Platform</p>
        </div>
    """
    
    return html

def get_confirmation_html(name, difficulty):
    """Generate confirmation page HTML (Gradio-compatible)."""
    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    css = """
        .confirmation-page {
            padding: 1.5rem;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .confirmation-title {
            color: var(--text-primary);
            font-size: 1.5rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 0.75rem;
        }
        
        .confirmation-subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            text-align: center;
            margin-bottom: 2rem;
            line-height: 1.5;
        }
        
        .user-details {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-sm);
        }
        
        .user-details ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .user-details li {
            padding: 0.75rem 0;
            color: var(--text-primary);
            font-size: 0.95rem;
            border-bottom: 1px solid var(--border-light);
            display: flex;
            justify-content: space-between;
        }
        
        .user-details li:last-child {
            border-bottom: none;
        }
        
        .detail-value {
            color: var(--primary);
            font-weight: 600;
        }
        
        .test-instructions {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-sm);
        }
        
        .test-instructions h4 {
            color: var(--text-primary);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .test-instructions ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .test-instructions li {
            padding: 0.5rem 0 0.5rem 1.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            position: relative;
            line-height: 1.4;
        }
        
        .test-instructions li::before {
            content: '•';
            position: absolute;
            left: 0;
            top: 0.5rem;
            color: var(--primary);
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .start-note {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));
            border: 1px solid var(--warning);
            border-radius: 12px;
            padding: 1.5rem;
            color: var(--text-primary);
            font-size: 0.9rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-sm);
        }
        
        .start-note strong {
            color: var(--warning);
        }
    """
    
    html = f"""
        <style>{css}</style>
        <div class="confirmation-page">
            <h3 class="confirmation-title">🎯 Ready to Begin Your PTE Assessment?</h3>
            <p class="confirmation-subtitle">You're all set! Review your details below and start your comprehensive PTE Academic evaluation.</p>
            
            <div class="user-details">
                <ul>
                    <li><strong>📝 Candidate Name:</strong> <span class="detail-value">{name}</span></li>
                    <li><strong>⚡ Difficulty Level:</strong> <span class="detail-value">{difficulty}</span></li>
                    <li><strong>⏱️ Total Duration:</strong> <span class="detail-value">20 minutes</span></li>
                    <li><strong>🔄 Assessment Rounds:</strong> <span class="detail-value">3 Comprehensive Sections</span></li>
                    <li><strong>📅 Assessment Date:</strong> <span class="detail-value">{current_date}</span></li>
                    <li><strong>🕐 Start Time:</strong> <span class="detail-value">{current_time}</span></li>
                </ul>
            </div>
            
            <div class="test-instructions">
                <h4>🎯 Essential Test Guidelines & Instructions</h4>
                <ul>
                    <li>Complete three comprehensive assessment rounds: Aptitude & Reasoning, Listening Comprehension, and Reading & Writing</li>
                    <li>Each round has specific time limits - effective time management is crucial for success</li>
                    <li>Answer all questions in each round before proceeding to the next section</li>
                    <li>Ensure stable internet connection throughout the entire assessment period</li>
                    <li>Enable audio and test your speakers/headphones for the listening comprehension section</li>
                    <li>Take the assessment in a quiet, distraction-free environment for optimal performance</li>
                    <li>Keep a notepad and pen handy for the writing section (recommended)</li>
                    <li>Do not refresh the browser or navigate away during the test</li>
                    <li>Your progress is automatically saved after each question</li>
                </ul>
            </div>
            
            <div class="start-note">
                <strong>⚠️ Important Notice:</strong> Once you click 'Start Assessment', the timer begins immediately and cannot be paused. Ensure you're fully prepared and ready to focus for the complete duration. Your session will be automatically saved and scored upon completion.
            </div>
        </div>
    """
    
    return html

def build_setup_ui():
    """Build and return the user setup UI components (Gradio-compatible)."""
    with gr.Column():
        components = {}
        
        # Header
        components["header"] = gr.HTML(get_header_html())
        
        # Test structure
        components["test_structure"] = gr.HTML(get_test_structure_html())
        
        # Setup form
        gr.HTML("<h3 style='color: var(--text-primary); text-align: center; margin: 2rem 0;'>📝 Enter Your Details</h3>")
        components["user_name_input"] = gr.Textbox(
            label="Enter your name:",
            placeholder="Your full name",
            max_lines=1,
            elem_classes="name-input"
        )
        
        components["difficulty_selector"] = gr.Dropdown(
            label="Select difficulty level:",
            choices=["Easy", "Medium", "Hard"],
            value="Easy"
        )
        
        components["start_btn"] = gr.Button(
            "🚀 Start Assessment Now",
            variant="primary",
            size="lg"
        )
        
        # Footer
        components["footer"] = gr.HTML(get_footer_html())
        
        return components

def build_confirmation_ui(name, difficulty):
    """Build confirmation page UI (Gradio-compatible)."""
    components = {}
    
    with gr.Column():
        # Header
        components["header"] = gr.HTML(get_header_html())
        
        # Confirmation details
        components["confirmation"] = gr.HTML(get_confirmation_html(name, difficulty))
        
        # Audio test section
        with gr.Accordion("🔊 Audio Test (Required for Full Experience)", open=False):
            gr.Markdown("**Test your audio setup before starting:**")
            gr.Audio(
                value="https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
                label="Test Audio",
                interactive=False
            )
            gr.Markdown("If you can hear the audio clearly, you're ready to proceed!")
        
        # Additional info accordions
        with gr.Accordion("📋 Test Structure & Scoring", open=False):
            gr.Markdown("""
            **Round 1: Aptitude & Reasoning (12 minutes)**
            - 20 logical reasoning questions
            - Pattern recognition and math problems
            - Adaptive difficulty adjustment
            - Score weight: 30%
            
            **Round 2: Listening Comprehension (3 minutes)**
            - 5 audio-based comprehension tasks
            - Fill-in-the-blank and multiple choice
            - Real-time audio playback
            - Score weight: 35%
            
            **Round 3: Reading & Writing (5 minutes)**
            - Reading passage analysis
            - Summary writing task (50-75 words)
            - Language proficiency evaluation
            - Score weight: 35%
            
            **Scoring System:**
            - Total possible score: 15 points (5 per section)
            - Detailed feedback and improvement suggestions
            - Personalized performance roadmap provided
            """)
        
        with gr.Accordion("💡 Performance Tips & Strategies", open=False):
            gr.Markdown("""
            **Before Starting:**
            - Ensure quiet environment without distractions
            - Close unnecessary browser tabs and applications
            - Have notepad ready for listening and writing sections
            - Check internet connection stability (minimum 1 Mbps)
            
            **During the Test:**
            - Read questions carefully before selecting answers
            - Manage time effectively - don't dwell on difficult questions
            - Use process of elimination for multiple choice options
            - Take brief notes during listening passages
            - Plan your summary structure before writing
            
            **Technical Tips:**
            - Use keyboard shortcuts when available
            - Avoid browser back/forward navigation buttons
            - Keep audio volume at comfortable listening level
            - Scroll slowly to avoid missing important content
            - Disable screen savers and power management settings
            """)
        
        with gr.Accordion("🆘 Technical Support & Troubleshooting", open=False):
            gr.Markdown("""
            **Before You Start - System Check:**
            - Browser: Chrome, Firefox, Safari, or Edge (latest version recommended)
            - Internet: Minimum 1 Mbps stable connection for audio streaming
            - Audio: Working speakers or headphones with microphone if needed
            - Screen: 1024x768 resolution or higher for optimal viewing
            
            **Common Issues & Solutions:**
            - **Audio not working:** Check browser permissions, volume levels, and try different browser
            - **Timer not starting:** Refresh page and restart the setup process
            - **Connection lost:** Test will auto-save progress; reconnect and continue
            - **Screen too small:** Zoom out (Ctrl/Cmd -) or use full-screen mode
            
            **Emergency Contact:**
            - Technical Support: support@ptera-mocktest.com
            - Phone: +1-800-PTE-HELP (24/7 availability)
            - Live Chat: Available during business hours via website
            
            **Quick Fixes:**
            - Clear browser cache and cookies before starting
            - Disable ad blockers and extensions temporarily
            - Use incognito/private browsing mode to avoid conflicts
            - Restart browser completely if experiencing persistent issues
            - Test audio playback in another tab first
            """)
        
        # Action buttons
        with gr.Row():
            components["confirm_start_btn"] = gr.Button(
                "🚀 Start Assessment Now",
                variant="primary",
                scale=3
            )
            components["edit_btn"] = gr.Button(
                "✏️ Edit Details",
                variant="secondary",
                scale=1
            )
            components["reset_btn"] = gr.Button(
                "🔄 Reset All",
                variant="secondary",
                scale=1
            )
        
        # Footer
        components["footer"] = gr.HTML(get_footer_html())
    
    return components

def build_results_ui():
    """Build results page UI (Gradio-compatible)."""
    components = {}
    
    with gr.Column():
        components["results_html"] = gr.HTML("""
            <div style='text-align: center; padding: 2rem;'>
                <h2 style='color: var(--text-primary);'>Your Test Results</h2>
                <p style='color: var(--text-secondary); font-size: 1rem;'>Your comprehensive score and detailed analysis will be displayed here after completing all sections.</p>
                <div style='margin-top: 1rem; font-size: 0.9rem; color: var(--text-muted);'>
                    <p>📊 Personalized performance breakdown</p>
                    <p>📈 Improvement recommendations</p>
                    <p>🎯 Next steps for PTE success</p>
                </div>
            </div>
        """)
        
        components["restart_btn"] = gr.Button(
            "🔄 Start New Test",
            variant="primary",
            size="lg"
        )
    
    return components