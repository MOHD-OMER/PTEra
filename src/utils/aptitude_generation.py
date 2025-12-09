"""
Aptitude question generation using Gemini 2.0 Flash with fallback to mock data.
"""
import random
import json
from typing import List, Dict, Any
from .base_utils import get_gemini_client, clean_json_content, ModelError, logger

# Full Mock Data: 20 Unique Easy Aptitude Questions (Math/Logic)
MOCK_QUESTIONS = [
    {
        "question": "What is 15 + 27?",
        "options": ["42", "41", "43", "40"],
        "correct": "42",
        "explanation": "Basic addition: 15 + 27 = 42."
    },
    {
        "question": "If a car travels 60 km in 2 hours, what is its speed?",
        "options": ["30 km/h", "120 km/h", "60 km/h", "20 km/h"],
        "correct": "30 km/h",
        "explanation": "Speed = distance / time = 60 / 2 = 30 km/h."
    },
    {
        "question": "Complete the sequence: 2, 4, 6, ?",
        "options": ["7", "8", "9", "10"],
        "correct": "8",
        "explanation": "Even numbers: +2 each time."
    },
    {
        "question": "What is 10% of 200?",
        "options": ["10", "20", "30", "40"],
        "correct": "20",
        "explanation": "10% = 10/100 = 0.1; 0.1 * 200 = 20."
    },
    {
        "question": "If A is B's brother, how is B related to A?",
        "options": ["Sister", "Brother", "Father", "Uncle"],
        "correct": "Brother",
        "explanation": "Brother is reciprocal."
    },
    {
        "question": "What is 5 * 8?",
        "options": ["40", "35", "45", "30"],
        "correct": "40",
        "explanation": "Multiplication table: 5 * 8 = 40."
    },
    {
        "question": "Next in series: 1, 3, 5, 7, ?",
        "options": ["8", "9", "10", "11"],
        "correct": "9",
        "explanation": "Odd numbers: +2 each."
    },
    {
        "question": "If 2 apples cost $4, how much for 5?",
        "options": ["$8", "$10", "$12", "$6"],
        "correct": "$10",
        "explanation": "Cost per apple = $2; 5 * $2 = $10."
    },
    {
        "question": "What is the square root of 16?",
        "options": ["2", "3", "4", "5"],
        "correct": "4",
        "explanation": "4 * 4 = 16."
    },
    {
        "question": "Logical pair: Pen : Write :: Knife : ?",
        "options": ["Cut", "Eat", "Read", "Draw"],
        "correct": "Cut",
        "explanation": "Function analogy."
    },
    {
        "question": "What is 100 - 45?",
        "options": ["55", "50", "60", "45"],
        "correct": "55",
        "explanation": "Subtraction: 100 - 45 = 55."
    },
    {
        "question": "Sequence: 10, 20, 30, ?",
        "options": ["35", "40", "45", "50"],
        "correct": "40",
        "explanation": "Multiples of 10: +10 each."
    },
    {
        "question": "If today is Monday, what day is 3 days later?",
        "options": ["Tuesday", "Wednesday", "Thursday", "Friday"],
        "correct": "Thursday",
        "explanation": "Monday + 3 = Thursday."
    },
    {
        "question": "What is 25 / 5?",
        "options": ["4", "5", "6", "3"],
        "correct": "5",
        "explanation": "Division: 25 ÷ 5 = 5."
    },
    {
        "question": "Odd one out: Apple, Banana, Carrot, Grape",
        "options": ["Apple", "Banana", "Carrot", "Grape"],
        "correct": "Carrot",
        "explanation": "Carrot is vegetable; others are fruits."
    },
    {
        "question": "What is 3 squared?",
        "options": ["6", "9", "12", "15"],
        "correct": "9",
        "explanation": "3 * 3 = 9."
    },
    {
        "question": "If X > Y and Y > Z, then?",
        "options": ["X < Z", "X = Z", "X > Z", "X = Y"],
        "correct": "X > Z",
        "explanation": "Transitive property."
    },
    {
        "question": "What is 50% of 80?",
        "options": ["30", "40", "50", "60"],
        "correct": "40",
        "explanation": "50% = 0.5; 0.5 * 80 = 40."
    },
    {
        "question": "Complete: Red, Blue, Green, ?",
        "options": ["Yellow", "Black", "White", "Orange"],
        "correct": "Yellow",
        "explanation": "Common color sequence (example; adapt as needed)."
    },
    {
        "question": "What is 12 * 3?",
        "options": ["36", "32", "40", "24"],
        "correct": "36",
        "explanation": "Multiplication: 12 * 3 = 36."
    }
]


def format_aptitude_prompt(difficulty: str, num_questions: int) -> str:
    """Format prompt for Gemini API to generate aptitude questions."""
    
    prompt = f"""You are an expert test creator. Generate {num_questions} aptitude questions for {difficulty} level.

CRITICAL REQUIREMENTS - FOLLOW EXACTLY:
1. Generate EXACTLY {num_questions} questions
2. Difficulty level: {difficulty}
3. Question types: Math, Logic, Reasoning, Patterns, Word Problems
4. Each question MUST have EXACTLY 4 options
5. Include clear explanations

OUTPUT FORMAT (pure JSON only, no markdown):
{{
    "questions": [
        {{
            "question": "What is 5 + 3?",
            "options": ["6", "7", "8", "9"],
            "correct": "8",
            "explanation": "Basic addition: 5 + 3 = 8"
        }},
        ... ({num_questions} questions total)
    ]
}}

IMPORTANT GUIDELINES:
- For {difficulty} level:
  * Easy: Basic arithmetic, simple patterns, straightforward logic
  * Medium: Multi-step problems, moderate reasoning, percentages
  * Hard: Complex calculations, advanced logic, data interpretation
- Each question must be clear and unambiguous
- Options should be plausible but have only ONE correct answer
- Explanations should be brief but clear (1-2 sentences)
- Output ONLY valid JSON (no ```json markers or extra text)
- Verify you generate EXACTLY {num_questions} questions

Remember: Count your questions carefully - you MUST generate exactly {num_questions} questions!"""
    
    return prompt


def parse_gemini_response(raw_content: str) -> List[Dict[str, Any]]:
    """Parse Gemini API response and extract questions."""
    try:
        # Clean the content
        cleaned = clean_json_content(raw_content)
        
        # Parse JSON
        data = json.loads(cleaned)
        
        # Extract questions
        if isinstance(data, dict) and "questions" in data:
            questions = data["questions"]
        elif isinstance(data, list):
            questions = data
        else:
            raise ModelError("Invalid response structure")
        
        logger.info(f"Parsed {len(questions)} questions from Gemini response")
        return questions
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        raise ModelError(f"Failed to parse JSON: {e}")
    except Exception as e:
        logger.error(f"Parsing error: {e}")
        raise ModelError(f"Failed to parse response: {e}")


def validate_aptitude_questions(questions: List[Dict[str, Any]], expected_count: int, flexible: bool = False) -> bool:
    """Validate aptitude questions structure."""
    try:
        if not isinstance(questions, list):
            logger.warning("Questions is not a list")
            return False
        
        # Flexible count validation
        if flexible:
            min_acceptable = int(expected_count * 0.85)  # Accept 85% on flexible
            logger.info(f"Flexible validation: accepting {min_acceptable}+ questions")
        else:
            min_acceptable = int(expected_count * 0.95)  # Accept 95% on strict
        
        if len(questions) < min_acceptable:
            logger.warning(f"Got {len(questions)} questions, need at least {min_acceptable}")
            return False
        
        # Validate each question
        for i, q in enumerate(questions[:expected_count], 1):
            if not isinstance(q, dict):
                logger.warning(f"Question {i} is not a dict")
                return False
            
            required_fields = ["question", "options", "correct", "explanation"]
            if not all(field in q for field in required_fields):
                logger.warning(f"Question {i} missing required fields")
                return False
            
            if not isinstance(q["options"], list) or len(q["options"]) != 4:
                logger.warning(f"Question {i} needs exactly 4 options")
                return False
            
            if q["correct"] not in q["options"]:
                logger.warning(f"Question {i} correct answer not in options")
                return False
        
        logger.info("✅ Aptitude questions validation passed")
        return True
    
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False


def generate_questions_multiround(difficulty: str, num_questions: int = 20) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate aptitude questions via Gemini 2.0 Flash or fallback to mocks.
    Returns: {"questions": List[Dict]}
    """
    max_retries = 2
    
    for attempt in range(max_retries):
        try:
            # Use flexible validation on retry
            use_flexible = (attempt > 0)
            
            logger.info(f"Attempting to generate {num_questions} {difficulty} aptitude questions via Gemini 2.0 (attempt {attempt + 1}/{max_retries})...")
            
            model = get_gemini_client()
            if model is None:
                raise ModelError("Gemini client is None - API key not configured")
            
            prompt = format_aptitude_prompt(difficulty, num_questions)
            logger.debug(f"Prompt length: {len(prompt)} chars")
            
            logger.info("Calling Gemini 2.0 Flash API...")
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 8000,
                }
            )
            
            if not response or not response.text:
                raise ModelError("Empty response from Gemini API")
            
            raw_content = response.text
            logger.debug(f"Raw response length: {len(raw_content)} chars")
            
            if not raw_content or len(raw_content.strip()) < 50:
                raise ModelError("Response content too short or empty")
            
            logger.info("Parsing Gemini response...")
            questions = parse_gemini_response(raw_content)
            
            if not questions:
                raise ModelError("Parsing returned empty list")
            
            logger.info(f"Parsed {len(questions)} questions from response")
            
            # Pad with mock questions if slightly short
            if len(questions) < num_questions:
                needed = num_questions - len(questions)
                logger.warning(f"Got {len(questions)}/{num_questions} questions, padding with {needed} mock questions")
                random.shuffle(MOCK_QUESTIONS)
                questions.extend(MOCK_QUESTIONS[:needed])
            
            # Validate the questions
            if validate_aptitude_questions(questions[:num_questions], num_questions, flexible=use_flexible):
                validation_type = "flexible" if use_flexible else "strict"
                logger.info(f"✅ Successfully generated {len(questions[:num_questions])} questions via Gemini 2.0 ({validation_type} validation)")
                return {"questions": questions[:num_questions]}
            
            raise ModelError("Question validation failed")
        
        except ModelError as e:
            logger.warning(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info("Retrying with more flexible criteria...")
                continue
            else:
                logger.error(f"❌ All {max_retries} attempts failed")
                break
        
        except Exception as e:
            logger.error(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
            if attempt < max_retries - 1:
                logger.info("Retrying...")
                continue
            else:
                break
    
    # Final fallback to mock data
    logger.info("Falling back to mock data...")
    random.shuffle(MOCK_QUESTIONS)
    return {"questions": MOCK_QUESTIONS[:num_questions]}