"""
Listening content generation with fill-blank and true/false/not-given questions only.
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
    """Get question type distribution based on difficulty (no MCQ)."""
    distributions = {
        "Easy": {"fill_blank": 3, "true_false_not_given": 2},
        "Medium": {"fill_blank": 3, "true_false_not_given": 2},
        "Hard": {"fill_blank": 2, "true_false_not_given": 3}
    }
    return distributions.get(difficulty, distributions["Easy"])


def validate_listening_content(data: Dict[str, Any], flexible: bool = False) -> bool:
    """Validate listening passage + questions structure (no MCQ)."""
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
            min_words = 100  # Very flexible for retry
            max_words = 350
            logger.info(f"Using flexible word count: {min_words}-{max_words}")
        else:
            min_words = 150
            max_words = 280
        
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

        logger.info("✅ Listening content validation passed")
        return True

    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False


def get_fallback_listening_content(difficulty="Easy"):
    """Fallback content with fill-blank and true/false/not-given questions only."""
    
    dist = get_question_distribution(difficulty)
    
    passage = """Reading books is one of the most beneficial habits a person can develop. Not only does reading improve vocabulary and language skills, but it also enhances critical thinking and concentration. When we read, our brains are actively engaged in processing information, which strengthens neural connections.

Studies have shown that regular readers tend to have better memory retention and are more empathetic towards others. Reading fiction, in particular, allows us to experience different perspectives and understand complex emotions. Additionally, reading before bed can help reduce stress and improve sleep quality.

In today's digital age, many people prefer scrolling through social media instead of reading books. However, researchers suggest that dedicating just 20-30 minutes a day to reading can significantly improve mental health and cognitive abilities. Whether it's fiction, non-fiction, or poetry, the act of reading offers countless benefits for people of all ages."""
    
    all_questions = [
        {
            "type": "fill_blank",
            "question": "Reading books improves vocabulary and __________ skills.",
            "correct_answer": "language",
            "skill": "detail"
        },
        {
            "type": "fill_blank",
            "question": "Regular readers tend to have better memory __________.",
            "correct_answer": "retention",
            "skill": "detail"
        },
        {
            "type": "fill_blank",
            "question": "Researchers suggest dedicating __________ minutes a day to reading.",
            "correct_answer": "20-30",
            "skill": "detail"
        },
        {
            "type": "fill_blank",
            "question": "Reading fiction helps us understand complex __________.",
            "correct_answer": "emotions",
            "skill": "detail"
        },
        {
            "type": "true_false_not_given",
            "question": "The passage states that reading before bed can help improve sleep quality.",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "True",
            "skill": "inference"
        },
        {
            "type": "true_false_not_given",
            "question": "The passage mentions that reading is more beneficial than watching educational videos.",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "Not Given",
            "skill": "inference"
        },
        {
            "type": "true_false_not_given",
            "question": "According to the passage, most people prefer reading books to using social media.",
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
        "title": "Benefits of Reading Books",
        "passage": passage,
        "questions": selected_questions
    }


def format_listening_prompt(difficulty: str) -> str:
    """Format prompt for Groq API to generate listening content (no MCQ)."""
    topic = get_random_topic()
    dist = get_question_distribution(difficulty)
    
    prompt = f"""You are an expert test creator. Generate a listening comprehension passage for {difficulty} level PTE test.

CRITICAL REQUIREMENTS - FOLLOW EXACTLY:
1. Passage MUST be 180-250 words (count carefully! This is for audio narration)
2. Topic: {topic}
3. EXACTLY 5 questions with this exact distribution:
   - {dist['fill_blank']} Fill in the Blank questions
   - {dist['true_false_not_given']} True/False/Not Given questions

IMPORTANT: Your passage MUST have AT LEAST 180 words. Short passages will be rejected.

OUTPUT FORMAT (pure JSON only, no markdown):
{{
    "title": "Engaging Title About {topic}",
    "passage": "Write a clear, well-structured passage of 180-250 words suitable for audio narration. Use conversational yet informative tone. Include specific details that can be tested. Make it appropriate for {difficulty} level listening comprehension. DO NOT write a short passage - aim for 200+ words with multiple paragraphs.",
    "questions": [
        {{
            "type": "fill_blank",
            "question": "The speaker mentions that something is __________.",
            "correct_answer": "answer",
            "skill": "detail"
        }},
        {{
            "type": "true_false_not_given",
            "question": "According to the audio, [statement].",
            "options": ["True", "False", "Not Given"],
            "correct_answer": "True",
            "skill": "inference"
        }}
    ]
}}

REMEMBER: 
- Passage MUST be 180-250 words (verify word count! Count every single word!)
- Write in natural speaking style (suitable for audio)
- Output ONLY valid JSON (no ```json or other markers)
- Include EXACTLY 5 questions (fill-blank and true/false/not-given only)
- Questions should test listening comprehension skills
- DO NOT write short passages - they will fail validation"""
    
    return prompt


def generate_listening_content(difficulty: str) -> Dict[str, Any]:
    """Generate listening passage + questions via Groq or fallback (no MCQ)."""
    
    max_retries = 2
    
    for attempt in range(max_retries):
        try:
            # Use flexible validation on retry
            use_flexible = (attempt > 0)
            
            logger.info(f"Attempting to generate {difficulty} listening content via Groq (attempt {attempt + 1}/{max_retries})...")
            
            client = get_groq_client()
            if client is None:
                raise ModelError("Groq client is None - API key not configured")
            
            prompt = format_listening_prompt(difficulty)
            logger.debug(f"Prompt length: {len(prompt)} chars")
            
            logger.info("Calling Groq API...")
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3500,
                timeout=45
            )
            
            if not response or not response.choices:
                raise ModelError("Empty response from Groq API")
            
            raw_content = response.choices[0].message.content
            logger.debug(f"Raw response length: {len(raw_content)} chars")
            
            cleaned_content = clean_json_content(raw_content)
            logger.debug(f"Cleaned content preview: {cleaned_content[:300]}...")
            
            data = json.loads(cleaned_content)
            
            logger.info("Validating listening content...")
            # Use flexible validation based on attempt
            if validate_listening_content(data, flexible=use_flexible):
                validation_type = "flexible" if use_flexible else "strict"
                logger.info(f"✅ Successfully generated listening content via Groq ({validation_type} validation)")
                return data
            else:
                raise ModelError("Listening content validation failed")
        
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
    return get_fallback_listening_content(difficulty)