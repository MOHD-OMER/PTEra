"""
Question generation, parsing, and validation utilities.
Now fully framework-agnostic and optimized for Gradio + Groq.
"""

from typing import List, Dict, Any
import json
import logging
import re

logger = logging.getLogger(__name__)


# ============================================================
# LOCAL ERROR CLASS (prevents circular import)
# ============================================================

class ModelError(Exception):
    """Custom error used for model parsing issues."""
    pass


# ============================================================
# LOCAL JSON CLEANER (prevents circular import)
# ============================================================

def clean_json_content(text: str) -> str:
    """
    Clean Groq output and extract valid JSON.
    Removes markdown, code blocks, text before/after JSON.
    """
    if not text:
        raise ModelError("Empty response from model.")

    # Remove markdown/code fences
    text = re.sub(r"```json|```", "", text).strip()

    # Extract JSON object between first { and last }
    if "{" in text and "}" in text:
        start = text.find("{")
        end = text.rfind("}") + 1
        text = text[start:end]

    # Remove trailing commas before }
    text = re.sub(r",\s*}", "}", text)

    return text


# ============================================================
# VALIDATION UTILITIES
# ============================================================

def validate_aptitude_questions(questions: List[Dict[str, Any]]) -> bool:
    """Validate aptitude question structure."""
    if not isinstance(questions, list):
        logger.error("Aptitude validation failed: questions must be a list")
        return False

    if len(questions) != 25:
        logger.error(f"Aptitude validation failed: expected 25 questions, got {len(questions)}")
        return False

    required_keys = {"question", "options", "correct", "explanation"}

    for idx, q in enumerate(questions, 1):

        if not isinstance(q, dict):
            logger.error(f"Question {idx} is not a dictionary")
            return False

        missing = required_keys - q.keys()
        if missing:
            logger.error(f"Question {idx} missing keys: {missing}")
            return False

        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            logger.error(f"Question {idx} must have exactly 4 options")
            return False

        if q["correct"] not in q["options"]:
            logger.error(f"Question {idx} correct answer '{q['correct']}' is not in options")
            return False

        if not q["question"].strip():
            logger.error(f"Question {idx} has empty question text")
            return False

        if not q["explanation"].strip():
            logger.error(f"Question {idx} has empty explanation")
            return False

        if any(not opt.strip() for opt in q["options"]):
            logger.error(f"Question {idx} contains an empty option")
            return False

    return True

def validate_aptitude_questions_flexible(
    questions: List[Dict[str, Any]],
    min_questions: int = 10
) -> bool:
    """
    Flexible validator:
    - Accepts ANY number >= min_questions
    - Only checks structure of each question
    - Used for early Groq attempts before strict validation
    """
    if not isinstance(questions, list):
        return False

    if len(questions) < min_questions:
        return False

    for i, q in enumerate(questions, start=1):
        if not isinstance(q, dict):
            return False
        
        # Basic required keys
        if not {"question", "options", "correct", "explanation"} <= q.keys():
            return False

        # Must have 4 options
        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            return False
        
        # No empty question
        if not q["question"].strip():
            return False

        # Options cannot be empty
        if any(not str(opt).strip() for opt in q["options"]):
            return False

        # Correct must be a non-empty string
        if not str(q["correct"]).strip():
            return False

    return True



def validate_listening_content(content: Dict[str, Any]) -> bool:
    """Validate listening round JSON structure."""
    required = {"passage", "blanks"}

    if not isinstance(content, dict):
        logger.error("Listening content is not a dictionary")
        return False

    if not required <= content.keys():
        logger.error(f"Listening content missing keys: {required - content.keys()}")
        return False

    wc = len(content["passage"].split())
    if wc < 200 or wc > 300:
        logger.error(f"Listening passage length invalid: {wc} words")
        return False

    if not isinstance(content["blanks"], list) or len(content["blanks"]) != 5:
        logger.error("Listening blanks must be a list of exactly 5 items")
        return False

    for idx, b in enumerate(content["blanks"], 1):

        if not isinstance(b, dict):
            logger.error(f"Blank {idx} is not a dictionary")
            return False

        if not {"context", "answer"} <= b.keys():
            logger.error(f"Blank {idx} missing required fields")
            return False

        if b["context"].count("___") != 1:
            logger.error(f"Blank {idx} must contain exactly one ___ placeholder")
            return False

        if not b["answer"].strip():
            logger.error(f"Blank {idx} has empty answer")
            return False

        if len(b["answer"].split()) > 1:
            logger.error(f"Blank {idx} answer must be a single word")
            return False

        if b["answer"].lower() not in content["passage"].lower():
            logger.error(f"Blank {idx} answer '{b['answer']}' not found in passage")
            return False

    return True


def validate_reading_content(content: Dict[str, Any]) -> bool:
    """Validate reading passage."""
    required = {"title", "passage", "key_points"}

    if not required <= content.keys():
        logger.error("Reading content missing required keys")
        return False

    wc = len(content["passage"].split())
    if wc < 200 or wc > 250:
        logger.error(f"Reading passage must be 200–250 words (got {wc})")
        return False

    if not isinstance(content["key_points"], list) or len(content["key_points"]) < 3:
        logger.error("Reading content must have at least 3 key points")
        return False

    return True


# ============================================================
# PROMPT GENERATORS
# ============================================================

def format_aptitude_prompt(difficulty: str, num_questions: int = 25) -> str:
    """Prompt for generating aptitude questions."""
    return f"""
Generate exactly {num_questions} {difficulty.lower()} level aptitude questions in this EXACT JSON format:

{{"questions":[
{{"question":"What is 2 + 2?","options":["3","4","5","6"],"correct":"4","explanation":"Basic addition"}}
]}}

Rules:
- EXACTLY {num_questions} questions
- All strings MUST use double quotes
- NO markdown, NO code fences, NO line breaks outside JSON
- Each question:
  - Has 4 options
  - 'correct' must match one option exactly
  - Includes a short explanation
- Difficulty: {difficulty}
- Types: sequences, logic, math word problems, patterns, relationships

Return ONLY a single-line JSON object.
""".strip()


def format_listening_prompt() -> str:
    """Prompt for generating listening passage."""
    return """
Generate an academic listening passage in EXACTLY this JSON format:

{
    "title": "...",
    "passage": "250 words separated into 5 paragraphs of 50 words each.",
    "blanks": [
        {"original_text": "...", "context": "Sentence with ___", "answer": "..."},
        {"original_text": "...", "context": "Sentence with ___", "answer": "..."},
        {"original_text": "...", "context": "Sentence with ___", "answer": "..."},
        {"original_text": "...", "context": "Sentence with ___", "answer": "..."},
        {"original_text": "...", "context": "Sentence with ___", "answer": "..."}
    ]
}

Rules:
- EXACTLY 5 blanks
- Each blank from a different paragraph
- Context must be a full sentence with ONE ___
- Return ONLY raw JSON, no explanation.
""".strip()


def format_reading_prompt() -> str:
    """Prompt for generating reading content."""
    return """
Generate a reading passage for a PTE summary task in this JSON format:

{
    "title": "Passage Title",
    "passage": "400–500 word academic passage",
    "key_points": ["...", "...", "..."]
}

Return ONLY the JSON object.
""".strip()


# ============================================================
# GROQ RESPONSE PARSER (Simplified + Robust)
# ============================================================

def parse_groq_response(response_text: str, content_type: str = "questions") -> Any:
    """
    Clean + parse Groq model output and return the expected structure.
    """
    if not response_text:
        raise ModelError("Groq returned an empty response.")

    try:
        cleaned = clean_json_content(response_text)
        parsed = json.loads(cleaned)

        # ---- Extract needed structure ----
        if content_type == "questions":
            if isinstance(parsed, dict) and "questions" in parsed:
                return parsed["questions"]
            if isinstance(parsed, list):
                return parsed
            raise ModelError("Invalid 'questions' JSON structure")

        elif content_type == "listening":
            if not validate_listening_content(parsed):
                raise ModelError("Listening content validation failed.")
            return parsed

        elif content_type == "reading":
            if not validate_reading_content(parsed):
                raise ModelError("Reading content validation failed.")
            return parsed

        else:
            raise ModelError(f"Unknown content type: {content_type}")

    except Exception as e:
        logger.error(f"Groq parsing failed: {str(e)}")
        raise ModelError(f"Failed to parse Groq response: {str(e)}")
