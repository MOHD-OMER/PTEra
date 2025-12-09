PTEra - Professional PTE Academic Mock Test Platform
<div align="center">
Master Your PTE Academic Success with Comprehensive Mock Testing
Features • Installation • Usage • Project Structure • Contributing
</div>

📋 Overview
PTEra is a sophisticated, feature-rich mock test application designed to simulate the PTE Academic examination experience. Built with modern web technologies and an elegant UI, it provides students with realistic test conditions, instant feedback, and detailed performance analytics.
🎯 What Makes PTEra Special?

Comprehensive Testing: Three complete assessment modules (Aptitude, Listening, Reading)
Real-Time Scoring: Instant performance evaluation with detailed breakdowns
Adaptive Difficulty: Choose from Easy, Medium, or Hard difficulty levels
Professional UI: Beautiful, modern interface with smooth animations
Timed Sections: Authentic exam conditions with automatic progression
Detailed Analytics: Personalized feedback and improvement recommendations


✨ Features
🎓 Three Assessment Modules
1. Aptitude Round (12 minutes)

20 carefully crafted questions
Multiple choice format
Real-time timer with visual warnings
Instant feedback on submission
Score normalization (0-5 scale)

2. Listening Comprehension (3 minutes)

Audio-based passage (generated via gTTS)
Mixed question types:

Multiple Choice Questions (MCQ)
Fill in the Blank
True/False/Not Given


Auto-play audio functionality
Simultaneous answer submission

3. Reading Comprehension (10 minutes)

Full-length reading passages
Diverse question formats
Word count display
Scrollable passage with beautiful typography
Comprehensive answer validation

🎨 Professional UI/UX

Modern Design System: Glass morphism, gradients, and smooth transitions
Responsive Layout: Works seamlessly on desktop and mobile
Dark/Light Elements: Premium color schemes with excellent contrast
Animated Components: Fade-ins, slides, and pulse effects
Progress Tracking: Visual indicators for test completion
Timer Warnings: Color-coded alerts for remaining time

📊 Results & Analytics

Performance Dashboard: Comprehensive score breakdown
Detailed Review: Question-by-question analysis
Visual Scoring: Beautiful score cards with performance indicators
Improvement Tips: Personalized recommendations
Study Plan Generator: Customized preparation strategies


🚀 Installation
Prerequisites

Python 3.10 or higher
pip (Python package manager)
Virtual environment (recommended)

Step-by-Step Setup

Clone the Repository

bash   git clone https://github.com/yourusername/ptera-mock-test.git
   cd ptera-mock-test

Create Virtual Environment

bash   # Windows
   python -m venv pte-env
   pte-env\Scripts\activate

   # macOS/Linux
   python3 -m venv pte-env
   source pte-env/bin/activate

Install Dependencies

bash   pip install -r requirements.txt

Configure Environment Variables

bash   # Create .env file in root directory
   cp .env.example .env
   
   # Add your API keys (if using AI content generation)
   GROQ_API_KEY=your_api_key_here

Run the Application

bash   python src/main.py

Access the Application

Open your browser and navigate to: http://localhost:7861




📦 Requirements
txtgradio>=4.0.0
python-dotenv>=1.0.0
gtts>=2.3.0
requests>=2.31.0
anthropic>=0.7.0  # Optional: for AI content generation
```

---

## 🎮 Usage

### Starting Your Test

1. **Home Page**
   - Enter your full name
   - Select difficulty level (Easy/Medium/Hard)
   - Click "🚀 Start Assessment Now"

2. **Aptitude Round**
   - Answer 20 multiple-choice questions
   - 12-minute time limit
   - Click "Next Question" to progress
   - Automatic submission when complete

3. **Listening Round**
   - Listen to the audio passage (auto-plays)
   - Answer 5 questions simultaneously
   - Mix of MCQ, Fill Blanks, and True/False questions
   - 3-minute time limit

4. **Reading Round**
   - Read the provided passage carefully
   - Answer 5 comprehension questions
   - 10-minute time limit
   - Submit all answers at once

5. **Results**
   - View comprehensive performance dashboard
   - Review each question with correct answers
   - Get personalized improvement tips
   - Access customized study plan

### Navigation

- **🏠 Home**: Return to setup page
- **📝 Test**: Access current test section
- **📊 Results**: View your test results
- **ℹ️ About**: Learn about PTEra features

---

## 📁 Project Structure
```
pte-mocktest/
│
├── assets/
│   └── audio/                  # Audio files directory
│       └── listening_passage.mp3
│
├── src/
│   ├── auth/                   # Authentication & session
│   │   ├── session.py          # Session state management
│   │   └── ui.py               # Auth UI components
│   │
│   ├── rounds/                 # Test round modules
│   │   ├── aptitude.py         # Aptitude assessment
│   │   ├── listening.py        # Listening comprehension
│   │   └── reading.py          # Reading comprehension
│   │
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   │   └── gradio_styles.css
│   │   └── logo.png
│   │
│   ├── utils/                  # Utility functions
│   │   ├── aptitude_generation.py    # Question generation
│   │   ├── listening_generation.py   # Audio content
│   │   ├── reading_generation.py     # Reading passages
│   │   ├── results.py                # Results processing
│   │   ├── scoring.py                # Score calculation
│   │   └── timer.py                  # Timer utilities
│   │
│   ├── config.py               # Configuration settings
│   ├── main.py                 # Application entry point
│   └── __init__.py
│
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── setup.py                    # Package setup

🎨 UI Components
Design System

Primary Color: #667eea → #764ba2 (Gradient)
Success: #10b981
Warning: #f59e0b
Danger: #ef4444
Typography: Inter & Outfit fonts

Key Components

Hero Section: Eye-catching gradient header with animations
Glass Cards: Modern translucent cards with backdrop blur
Timer Badge: Animated countdown with color-coded warnings
Score Cards: Beautiful gradient score displays
Question Cards: Styled containers with type-specific colors
Navigation Bar: Smooth transitions between sections
Footer: Social links and copyright information


🔧 Configuration
Environment Variables
env# .env file
GROQ_API_KEY=your_groq_api_key_here
DEBUG=False
PORT=7861
HOST=0.0.0.0
Customization
Modify Timer Durations
python# In respective round files
state["aptitude_limit"] = 720   # 12 minutes
state["listen_limit"] = 180     # 3 minutes
state["reading_limit"] = 600    # 10 minutes
Change Difficulty Settings
python# In generation files
DIFFICULTY_LEVELS = {
    "Easy": {...},
    "Medium": {...},
    "Hard": {...}
}

🤝 Contributing
We welcome contributions! Here's how you can help:
Ways to Contribute

Report Bugs: Open an issue with detailed information
Suggest Features: Share your ideas for improvements
Submit Pull Requests: Fix bugs or add features
Improve Documentation: Help make the docs better
Share Feedback: Let us know your experience

Contribution Guidelines

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request


🐛 Troubleshooting
Common Issues
1. Audio Not Playing
bash# Ensure gTTS is installed
pip install gtts --upgrade

# Check audio file permissions
chmod 644 assets/audio/*.mp3
2. Import Errors
bash# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
3. Port Already in Use
python# Change port in main.py
app.launch(server_port=7862)  # Use different port
4. Timer Not Working
python# Ensure state is properly initialized
state = initialize_session_state()

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

Gradio: For the amazing UI framework
gTTS: For text-to-speech functionality
Python Community: For excellent libraries and support
PTE Academic: For inspiration and test format guidelines


📧 Contact & Support

Email: support@ptera.com
Issues: GitHub Issues
Discussions: GitHub Discussions


🗺️ Roadmap
Upcoming Features

 User authentication and profiles
 Progress tracking across multiple attempts
 Speaking module integration
 Writing assessment module
 Advanced analytics dashboard
 Export results as PDF
 Mobile app version
 Multi-language support
 AI-powered question generation
 Peer comparison features


📊 Statistics
<div align="center">
Show Image
Show Image
Show Image
Show Image
</div>

<div align="center">
Made with ❤️ for PTE Academic aspirants
⭐ Star this repository if you find it helpful!
</div>