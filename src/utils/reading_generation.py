"""
Reading content generation with fill_blank and true_false_not_given questions only.
"""

from typing import Dict, Any, List
import json
import random

from .base_utils import (
    get_groq_client,
    clean_json_content,
    get_random_topic,
    ModelError,
    logger,
)


def get_question_distribution(difficulty):
    """Get question type distribution based on difficulty."""
    distributions = {
        "Easy": {"fill_blank": 3, "true_false_not_given": 2},
        "Medium": {"fill_blank": 3, "true_false_not_given": 2},
        "Hard": {"fill_blank": 2, "true_false_not_given": 3}
    }
    return distributions.get(difficulty, distributions["Easy"])


def validate_reading_content(data: Dict[str, Any], flexible: bool = False) -> bool:
    """Validate reading passage + mixed questions structure."""
    try:
        required = {"title", "passage", "questions"}
        if not all(k in data for k in required):
            logger.warning(f"Missing required keys. Got: {data.keys()}")
            return False

        if not isinstance(data["passage"], str):
            logger.warning("Passage is not a string")
            return False

        words = len(data["passage"].split())
        
        # Adjust word count based on validation mode
        if flexible:
            min_words = 120  # Very flexible for retry
            max_words = 500
            logger.info(f"Using flexible word count: {min_words}-{max_words}")
        else:
            min_words = 200
            max_words = 400
        
        if words < min_words or words > max_words:
            logger.warning(f"Passage word count: {words} (target: {min_words}-{max_words})")
            if not flexible:
                return False

        if not isinstance(data["questions"], list) or len(data["questions"]) != 5:
            logger.warning(f"Need exactly 5 questions, got {len(data.get('questions', []))}")
            return False

        for i, q in enumerate(data["questions"], 1):
            if not isinstance(q, dict):
                logger.warning(f"Question {i} is not a dict")
                return False
            
            if "type" not in q or "question" not in q or "correct_answer" not in q:
                logger.warning(f"Question {i} missing required fields")
                return False
            
            q_type = q["type"]
            if q_type not in ["fill_blank", "true_false_not_given"]:
                logger.warning(f"Question {i} has invalid type: {q_type}")
                return False
            
            if q_type == "true_false_not_given" and (not isinstance(q.get("options"), list) or len(q["options"]) != 3):
                logger.warning(f"Question {i} (T/F/NG) needs 3 options")
                return False

        logger.info("✅ Reading content validation passed")
        return True

    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False


def get_fallback_reading_content(difficulty="Easy"):
    """Fallback content with fill_blank and true_false_not_given questions only."""
    
    dist = get_question_distribution(difficulty)
    
    passage = """Sleep is essential for maintaining good health and well-being. During sleep, our bodies repair tissues, consolidate memories, and regulate hormones. Most adults need between 7 to 9 hours of sleep each night to function optimally.

Lack of sleep can lead to various health problems. People who don't get enough sleep often experience mood swings, difficulty concentrating, and weakened immune systems. Chronic sleep deprivation has been linked to serious conditions such as obesity, diabetes, and heart disease.

Creating a good sleep routine can significantly improve sleep quality. Experts recommend going to bed and waking up at the same time every day, even on weekends. It's also helpful to avoid screens before bedtime, as the blue light emitted by phones and computers can interfere with the body's natural sleep cycle. Additionally, keeping the bedroom cool, dark, and quiet creates an ideal environment for restful sleep.

In today's fast-paced world, many people sacrifice sleep to meet work or social demands. However, prioritizing sleep is crucial for long-term health and productivity. Getting adequate rest allows us to think clearly, make better decisions, and maintain emotional balance."""
    
    all_questions = [
        {
            "type": "fill_blank",
            "question": "During sleep, our bodies repair tissues, consolidate memories, and regulate __________.",
            "correct_answer": "hormones",
            "skill": "detail"
        },
        {
            "type": "fill_blank",
            "question": "Chronic sleep deprivation has been linked to serious conditions such as obesity, diabetes, and __________ disease.",
            "correct_answer": "heart",
            "skill": "detail"
        },
        {
            "type": "fill_blank",
            "question": "Blue light emitted by screens can interfere with the body's natural __________ cycle.",
            "correct_answer": "sleep",
            "skill": "detail"
        },
        {
            "type": "fill_blank",
            "question": "Most adults need between 7 to 9 hours of __________ each night to function optimally.",
            "correct_answer": "sleep",
            "skill": "detail"
        },
        {
            "type": "true_false_not_given",
            "question": "The passage states that experts recommend going to bed at the same time every day.",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "True",
            "skill": "inference"
        },
        {
            "type": "true_false_not_given",
            "question": "According to the passage, napping during the day improves overall sleep quality.",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "Not Given",
            "skill": "inference"
        },
        {
            "type": "true_false_not_given",
            "question": "The passage suggests that most people get enough sleep in today's world.",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "False",
            "skill": "inference"
        }
    ]
    
    selected_questions = []
    fill_questions = [q for q in all_questions if q["type"] == "fill_blank"]
    tfng_questions = [q for q in all_questions if q["type"] == "true_false_not_given"]
    
    random.shuffle(fill_questions)
    random.shuffle(tfng_questions)
    
    selected_questions.extend(fill_questions[:dist["fill_blank"]])
    selected_questions.extend(tfng_questions[:dist["true_false_not_given"]])
    
    random.shuffle(selected_questions)
    
    return {
        "title": "The Importance of Sleep",
        "passage": passage,
        "questions": selected_questions
    }


def format_reading_prompt(difficulty: str) -> str:
    """Format prompt for Groq API to generate reading content."""
    topic = get_random_topic()
    dist = get_question_distribution(difficulty)
    
    prompt = f"""You are an expert test creator. Generate a reading comprehension passage for {difficulty} level PTE test.

CRITICAL REQUIREMENTS - FOLLOW EXACTLY:
1. Passage MUST be 250-350 words (count carefully!)
2. Topic: {topic}
3. EXACTLY 5 questions with this exact distribution:
   - {dist['fill_blank']} Fill in the Blank questions
   - {dist['true_false_not_given']} True/False/Not Given questions

IMPORTANT: Your passage MUST have AT LEAST 250 words. Short passages will be rejected.

OUTPUT FORMAT (pure JSON only, no markdown):
{{
    "title": "Engaging Title About {topic}",
    "passage": "Write a well-structured passage of 250-350 words here. Include multiple paragraphs (3-4 paragraphs recommended). Make it informative and suitable for {difficulty} level. The passage should have enough detail to support 5 different questions. DO NOT write a short passage - aim for 280+ words with detailed content.",
    "questions": [
        {{
            "type": "fill_blank",
            "question": "The passage mentions that something is __________.",
            "correct_answer": "answer",
            "skill": "detail"
        }},
        {{
            "type": "true_false_not_given",
            "question": "According to the passage, [statement].",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "True",
            "skill": "inference"
        }}
    ]
}}

REMEMBER: 
- Passage MUST be 250-350 words (verify word count! Count every single word!)
- Output ONLY valid JSON (no ```json or other markers)
- Include EXACTLY 5 questions (NO multiple choice questions)
- Only use fill_blank and true_false_not_given question types
- Make questions test different comprehension skills
- Write DETAILED passages with multiple paragraphs - short passages fail validation"""
    
    return prompt


def generate_reading_content(difficulty: str) -> Dict[str, Any]:
    """Generate reading passage + mixed questions via Groq or fallback."""
    
    max_retries = 2
    
    for attempt in range(max_retries):
        try:
            # Use flexible validation on retry
            use_flexible = (attempt > 0)
            
            logger.info(f"Attempting to generate {difficulty} reading content via Groq (attempt {attempt + 1}/{max_retries})...")
            
            client = get_groq_client()
            if client is None:
                raise ModelError("Groq client is None - API key not configured")
            
            prompt = format_reading_prompt(difficulty)
            logger.debug(f"Prompt length: {len(prompt)} chars")
            
            logger.info("Calling Groq API...")
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000,
                timeout=45
            )
            
            if not response or not response.choices:
                raise ModelError("Empty response from Groq API")
            
            raw_content = response.choices[0].message.content
            logger.debug(f"Raw response length: {len(raw_content)} chars")
            
            cleaned_content = clean_json_content(raw_content)
            logger.debug(f"Cleaned content preview: {cleaned_content[:300]}...")
            
            data = json.loads(cleaned_content)
            
            logger.info("Validating reading content...")
            # Use flexible validation based on attempt
            if validate_reading_content(data, flexible=use_flexible):
                validation_type = "flexible" if use_flexible else "strict"
                logger.info(f"✅ Successfully generated reading content via Groq ({validation_type} validation)")
                return data
            else:
                raise ModelError("Reading content validation failed")
        
        except ModelError as e:
            logger.warning(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info("Retrying with more flexible criteria...")
                continue
            else:
                logger.error(f"❌ All {max_retries} attempts failed")
                break
        
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing error: {str(e)}")
            if attempt < max_retries - 1:
                logger.info("Retrying...")
                continue
            else:
                break
        
        except Exception as e:
            logger.error(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
            if attempt < max_retries - 1:
                logger.info("Retrying...")
                continue
            else:
                break
    
    logger.info("Falling back to mock data...")
    return get_fallback_reading_content(difficulty)