"""Scoring and evaluation utilities for PTE Mock Test."""
from typing import List, Dict, Any
from collections import Counter
import re
from statistics import mean, stdev

def clean_text(text: str) -> str:
    """Clean and normalize text for comparison."""
    # Remove punctuation and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    # Convert to lowercase and normalize whitespace
    return ' '.join(text.lower().split())

def get_text_stats(text: str) -> Dict[str, Any]:
    """Get basic text statistics."""
    words = text.split()
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
        'unique_words': len(set(words))
    }

def normalize_score(raw_score: int, max_raw_score: int, max_normalized: int = 5) -> int:
    """Normalize a raw score to a scale (default 0-5)."""
    if not isinstance(raw_score, (int, float)) or not isinstance(max_raw_score, (int, float)):
        raise ValueError("Scores must be numeric")
    if max_raw_score <= 0:
        raise ValueError("Maximum score must be positive")
    if raw_score < 0:
        raise ValueError("Raw score cannot be negative")
    
    normalized = round((raw_score / max_raw_score) * max_normalized)
    return min(max_normalized, max(0, normalized))

def evaluate_answers(user_answers: List[str], questions: List[Dict[str, Any]], answer_key: str = 'correct', options_key: str = 'options') -> Dict[str, Any]:
    """Generic answer evaluation function."""
    if not isinstance(user_answers, list) or not isinstance(questions, list):
        raise ValueError("Invalid input types")
    if len(user_answers) != len(questions):
        raise ValueError("Number of answers does not match number of questions")
    
    correct_count = 0
    results = []
    
    for idx, (answer, question) in enumerate(zip(user_answers, questions)):
        if not isinstance(question, dict):
            raise ValueError(f"Invalid question format at index {idx}")
        
        # For listening questions, correct answer is first option
        correct_answer = (question[options_key][0] if options_key in question 
                         else question.get(answer_key))
        if not correct_answer:
            raise ValueError(f"No correct answer found for question {idx}")
        
        is_correct = answer == correct_answer
        if is_correct:
            correct_count += 1
        
        result = {
            'question_number': idx + 1,
            'is_correct': is_correct,
            'user_answer': answer,
            'correct_answer': correct_answer
        }
        
        # Add optional fields if present
        for field in ['explanation', 'context', 'original_text']:
            if field in question:
                result[field] = question[field]
        
        results.append(result)
    
    return {
        'raw_score': correct_count,
        'normalized_score': normalize_score(correct_count, len(questions)),
        'total_questions': len(questions),
        'accuracy_percentage': (correct_count / len(questions)) * 100,
        'results': results
    }

def evaluate_aptitude_answers(user_answers: List[str], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate aptitude round answers.
    
    Each question is worth 0.25 points, with a maximum of 5 points for 20 questions.
    """
    result = evaluate_answers(user_answers, questions)
    # Update scoring for 20 questions worth 0.25 points each
    raw_score = result['raw_score']
    result['points_per_question'] = 0.25
    result['raw_points'] = raw_score * 0.25
    result['normalized_score'] = min(5, result['raw_points'])  # Cap at 5 points
    return result

def evaluate_listening_answers(user_answers: List[str], content: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate listening round answers.
    
    Each question is worth 1 point, with a maximum of 5 points for 5 questions.
    """
    if not isinstance(content, dict) or 'blanks' not in content:
        raise ValueError("Invalid content format")
    result = evaluate_answers(user_answers, content['blanks'], options_key='options')
    # Each question worth 1 point
    result['points_per_question'] = 1
    result['raw_points'] = result['raw_score']  # Direct 1:1 scoring
    result['normalized_score'] = result['raw_score']  # No normalization needed
    return result

def evaluate_summary(summary_text: str, key_points: List[str], min_words: int = 50) -> Dict[str, Any]:
    """Evaluate reading round summary.
    
    Scoring criteria:
    - Word count requirement (min 50 words): 1 point
    - Key points coverage (up to 3 points)
    - Writing quality (coherence, grammar, vocabulary): 1 point
    Total: 5 points maximum
    """
    if not summary_text or not key_points:
        return {
            'raw_score': 0,
            'normalized_score': 0,
            'word_count': 0,
            'covered_points': [],
            'feedback': ["No summary or key points provided"]
        }
    
    # Text analysis
    stats = get_text_stats(summary_text)
    word_count = stats['word_count']
    score = 0
    feedback = []
    
    # Word count scoring (1 point)
    if word_count >= min_words:
        score += 1
        feedback.append("✓ Met minimum word requirement")
    else:
        feedback.append(f"✗ Below minimum word requirement ({word_count}/{min_words} words)")
    
    # Key points coverage (up to 3 points)
    covered_points = []
    summary_clean = clean_text(summary_text)
    key_points_clean = [clean_text(point) for point in key_points]
    
    for original_point, clean_point in zip(key_points, key_points_clean):
        keywords = clean_point.split()
        matches = sum(1 for word in keywords if word in summary_clean)
        if matches >= len(keywords) * 0.6:  # 60% threshold
            covered_points.append(original_point)
    
    coverage_score = min(3, round(len(covered_points) / len(key_points) * 3))
    score += coverage_score
    
    # Writing quality scoring (1 point)
    quality_score = 0
    if stats['avg_words_per_sentence'] <= 25:  # Good sentence length
        quality_score += 0.5
    if stats['unique_words'] >= word_count * 0.4:  # Good vocabulary variety
        quality_score += 0.5
    score += round(quality_score)
    
    # Generate detailed feedback
    feedback.extend(_generate_summary_feedback(
        normalized_score=score,
        word_count=word_count,
        stats=stats
    ))
    
    return {
        'raw_score': score,
        'normalized_score': score,  # Already on 5-point scale
        'word_count': word_count,
        'text_stats': stats,
        'covered_points': covered_points,
        'coverage_percentage': (len(covered_points) / len(key_points)) * 100,
        'feedback': feedback
    }

def _generate_summary_feedback(normalized_score: int, word_count: int, stats: Dict[str, Any]) -> List[str]:
    """Generate feedback for summary evaluation."""
    feedback = []
    
    # Score feedback
    if normalized_score == 5:
        feedback.append("Excellent coverage of all key points!")
    elif normalized_score >= 3:
        feedback.append("Good coverage of main points.")
    else:
        feedback.append("Some key points were missed.")
    
    # Length feedback
    if word_count > 200:
        feedback.append("Summary is quite detailed but could be more concise.")
    elif word_count < 100:
        feedback.append("Consider expanding the summary with more details.")
    
    # Structure feedback
    if stats['avg_words_per_sentence'] > 25:
        feedback.append("Consider using shorter, clearer sentences.")
    if stats['unique_words'] < word_count * 0.4:
        feedback.append("Try using more varied vocabulary.")
    
    return feedback

def calculate_final_score(scores: Dict[str, int]) -> Dict[str, Any]:
    """Calculate final test score and provide feedback.
    
    Maximum score is 15 points (5 points per section).
    Performance levels:
    - Excellent: 80% or higher (12-15 points)
    - Good: 60-79% (9-11 points)
    - Needs Improvement: Below 60% (0-8 points)
    """
    if not scores or not all(isinstance(v, (int, float)) for v in scores.values()):
        raise ValueError("Invalid scores format")
    
    score_values = list(scores.values())
    total_score = sum(score_values)
    max_score = len(scores) * 5  # 5 points per round
    percentage = (total_score / max_score) * 100
    
    # Calculate statistics
    avg_score = mean(score_values)
    std_dev = stdev(score_values) if len(score_values) > 1 else 0
    
    # Identify strengths and improvements needed
    strengths = [round for round, score in scores.items() if score > avg_score]
    improvements = [round for round, score in scores.items() if score < avg_score]
    
    return {
        'total_score': total_score,
        'max_score': max_score,
        'percentage': percentage,
        'performance_level': _get_performance_level(percentage),
        'strengths': strengths,
        'improvements': improvements,
        'scores_by_round': dict(scores),
        'average_score': avg_score,
        'score_std_dev': std_dev,
        'feedback': _generate_final_feedback(percentage, std_dev, strengths, improvements)
    }

def _get_performance_level(percentage: float) -> str:
    """Get performance level based on percentage score."""
    if percentage >= 80:
        return "Excellent"
    elif percentage >= 60:
        return "Good"
    return "Needs Improvement"

def _generate_final_feedback(percentage: float, std_dev: float, strengths: List[str], improvements: List[str]) -> List[str]:
    """Generate feedback for final score."""
    feedback = []
    
    # Overall performance feedback
    if percentage >= 80:
        feedback.append("Outstanding performance across all sections!")
    elif percentage >= 60:
        feedback.append("Good overall performance with room for improvement.")
    else:
        feedback.append("Additional practice recommended to improve scores.")
    
    # Consistency feedback
    if std_dev < 1:
        feedback.append("Very consistent performance across all sections.")
    elif std_dev > 2:
        feedback.append("Performance varies significantly between sections.")
    
    # Section-specific feedback
    if strengths:
        feedback.append(f"Strong performance in: {', '.join(strengths)}")
    if improvements:
        feedback.append(f"Focus on improving: {', '.join(improvements)}")
    
    return feedback 