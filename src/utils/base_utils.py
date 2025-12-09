import os
import json
import logging
import re
from typing import Dict, Any, Optional
from groq import Groq
import httpx
import random
from .questions import parse_groq_response

# -----------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------
# Custom Error
# -----------------------------------------------------------

class ModelError(Exception):
    """Custom exception for model or response errors."""
    pass


# -----------------------------------------------------------
# Groq Client
# -----------------------------------------------------------

def get_groq_client() -> Groq:
    """
    Initialize and return Groq client safely.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("❌ GROQ_API_KEY is missing from environment variables.")
        raise ModelError("GROQ_API_KEY environment variable not set")

    try:
        # Force a plain httpx client to avoid incompatibilities with patched clients
        # that may not support proxy parameters.
        http_client = httpx.Client()
        return Groq(api_key=api_key, http_client=http_client)
    except Exception as e:
        logger.error(f"Failed to initialize Groq client: {str(e)}")
        raise ModelError(f"Failed to initialize Groq client: {str(e)}")


# -----------------------------------------------------------
# Gemini Client
# -----------------------------------------------------------

def get_gemini_client():
    """
    Initialize and return Gemini 2.0 Flash client.
    Returns the generative model instance.
    """
    try:
        import google.generativeai as genai
       
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment")
            return None
       
        genai.configure(api_key=api_key)
       
        # Use Gemini 2.0 Flash model
        model = genai.GenerativeModel("gemini-1.5-flash")
       
        logger.info("✅ Gemini  1.5 Flash client initialized")
        return model
   
    except ImportError:
        logger.error("google-generativeai package not installed. Run: pip install google-generativeai")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        return None


# -----------------------------------------------------------
# JSON Cleaning Utility
# -----------------------------------------------------------

def clean_json_content(content: str) -> str:
    """
    Clean malformed JSON returned by LLMs.
    Ensures output is a valid JSON string.

    Returns: str (json.dumps(valid_dict))
    """
    original_content = content

    try:
        # Remove code fences
        content = content.strip()
        content = re.sub(r"^```json", "", content, flags=re.IGNORECASE)
        content = re.sub(r"^```", "", content)
        content = re.sub(r"```$", "", content)
        content = content.strip()

        # First quick parse attempt
        try:
            parsed = json.loads(content)
            return json.dumps(parsed)
        except json.JSONDecodeError:
            pass

        # Normalize bad quotes
        content = (
            content.replace("“", '"')
                   .replace("”", '"')
                   .replace("‘", "'")
                   .replace("’", "'")
        )

        # Replace single quotes with double quotes (JSON-safe)
        content = re.sub(r"'", '"', content)

        # Remove stray trailing commas
        content = re.sub(r",\s*([}\]])", r"\1", content)

        # Ensure it starts and ends with braces
        if not content.startswith("{"):
            content = "{" + content
        if not content.endswith("}"):
            content = content + "}"

        # Fix common malformed key:value breakages
        content = re.sub(r'"\s*:\s*"', '":"', content)
        content = re.sub(r'\s+', ' ', content)

        # Try final cleaning
        parsed = json.loads(content)
        return json.dumps(parsed)

    except Exception as e:
        logger.error(
            f"JSON cleaning failed: {str(e)}\n"
            f"Original Content:\n{original_content}\n"
            f"After Cleaning:\n{content}"
        )
        raise ModelError(f"Failed to clean JSON content: {str(e)}")


# -----------------------------------------------------------
# Topic Generator
# -----------------------------------------------------------

def get_random_topic() -> str:
    """
    Returns a random academic topic for text generation.
    """
    topics = [
        "environmental conservation",
        "digital technology",
        "global education",
        "public health",
        "cultural diversity",
        "urban development",
        "scientific research",
        "economic growth",
        "social media impact",
        "renewable energy",
        "artificial intelligence",
        "climate change",
        "online learning",
        "transportation systems",
        "workplace communication",
        "international trade",
        "mental wellbeing",
        "sustainable living",
        "innovation trends",
        "community development",
        "Technology and Innovation",
        "Health and Wellness",
        "Education Systems",
        "Space Exploration",
        "Cultural Heritage",
        "Modern Transportation",
        "Digital Communication",
        "Scientific Discoveries",
        "Global Economics"
    ]
    return random.choice(topics)

# Add any other utility functions you need here...