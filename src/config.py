"""Configuration settings for PTE Mock Test."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Development mode flag
DEV_MODE = os.getenv('DEV_MODE', 'false').lower() == 'true'

# API Keys
GROQ_API_KEYS = {
    'aptitude': os.getenv('GROQ_APTITUDE_KEY', 'dummy_key_aptitude'),
    'listening': os.getenv('GROQ_LISTENING_KEY', 'dummy_key_listening'),
    'reading': os.getenv('GROQ_READING_KEY', 'dummy_key_reading')
}

# Question settings for each round
QUESTION_SETTINGS = {
    'aptitude': {
        'num_questions': 5,
        'categories': [
            'Mathematics',
            'Logical Reasoning',
            'Verbal Reasoning'
        ],
        'difficulty_levels': [
            'Easy',
            'Medium',
            'Hard'
        ]
    },
    'listening': {
        'num_passages': 2,
        'questions_per_passage': 3,
        'topics': [
            'Technology',
            'Science',
            'Environment',
            'Education',
            'Culture'
        ]
    },
    'reading': {
        'num_passages': 2,
        'questions_per_passage': 3,
        'topics': [
            'Technology',
            'Science',
            'Environment',
            'Education',
            'Culture'
        ]
    }
} 