# PTE Mock Test Application

A Gradio-based PTE (Pearson Test of English) mock test application with dynamic content generation via Groq LLM and text-to-speech for listening passages.

## Features

- Three test rounds: Aptitude, Listening, and Reading
- Dynamic question generation using Groq LLM
- Text-to-speech for listening comprehension
- Timed sections with automatic progression
- Detailed performance feedback
- Difficulty level selection
- Progress tracking and scoring
- Responsive UI design with dark mode
- Session state management
- Error handling and recovery
- Custom styling with Google Fonts integration

## Project Structure

```
pte-mocktest/
├── src/
│   ├── main.py           # Main application entry point
│   ├── config.py         # Configuration settings
│   ├── __init__.py       # Package initialization
│   ├── auth/             # Authentication and session management
│   ├── rounds/           # Test round implementations
│   ├── static/           # Static assets (CSS, images)
│   └── utils/            # Utility functions
├── assets/               # Application assets
├── requirements.txt      # Project dependencies
├── setup.py             # Package setup configuration
└── README.md            # Project documentation
```

## Technical Architecture

### Frontend
- Gradio Blocks UI with custom CSS
- Session state navigation across rounds

### Backend
- Python 3.8+ runtime
- Groq LLM integration for aptitude question generation (model: `llama-3.1-8b-instant`)
- gTTS (Google Text-to-Speech) for listening audio generation
- httpx for HTTP calls

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd pte-mocktest
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Run the application:
```bash
python src/main.py
```

## Test Structure

### 1. Aptitude Round
- 5 multiple-choice questions
- 15 minutes time limit
- Questions generated based on difficulty level
- Instant feedback on completion
- Error recovery and retry options

### 2. Listening Round
- Audio passage with mixed questions (MCQ, fill-in-the-blank, True/False/Not Given)
- 3 minutes time limit
- Text-to-speech generated content
- Audio playback controls

### 3. Reading Round
- Academic passage with mixed questions (MCQ, fill-in-the-blank, True/False/Not Given)
- 10 minutes total
- Timer with visual indicators

## Scoring System

Each round is scored out of 5 points:
- Aptitude: Based on correct answers
- Listening: Based on correct fill-in-the-blanks
- Reading: Based on key points covered in summary

Total maximum score: 15 points

## Development

### Requirements
- Python 3.8+
- Groq API key (`GROQ_API_KEY`)
- Internet connection for TTS and LLM features
- Audio output capability
- Key dependencies (see `requirements.txt` for full list):
  - gradio
  - groq
  - gTTS
  - httpx
  - python-dotenv

### Error Handling
The application implements comprehensive error handling:
- Content generation failures
- Network connectivity issues
- Session state corruption
- API rate limiting
- Audio playback errors

### Testing
To run tests:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request



## Acknowledgments

- Streamlit team for the excellent framework
- Groq for the LLM API
- Contributors and testers
