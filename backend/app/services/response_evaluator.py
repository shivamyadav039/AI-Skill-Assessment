"""
Response Evaluator Service - NLP-based evaluation of candidate responses.

Phase 3: Replace placeholder quality scoring with real NLP-based evaluation.

Features:
- Semantic similarity scoring
- Keyword/concept matching
- Response coherence analysis
- Confidence scoring based on evidence
- Multi-faceted evaluation
"""

from typing import List, Dict, Tuple, Optional, Any
from loguru import logger

try:
    from sentence_transformers import SentenceTransformer, util
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("sentence-transformers not available - using fallback evaluation")
    TRANSFORMERS_AVAILABLE = False


class ResponseEvaluator:
    """Evaluate candidate responses for quality and relevance."""
    
    def __init__(self):
        """Initialize the response evaluator."""
        self.model = None
        self.quality_keywords = {
            "high": ["specific", "example", "project", "implemented", "achieved", "learned", 
                    "solved", "challenge", "experience", "demonstrated", "successfully", "results"],
            "medium": ["used", "worked", "familiar", "understand", "know", "experience"],
            "low": ["yeah", "basically", "kinda", "um", "like", "i think"]
        }
        
        if TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("✅ Response Evaluator initialized with sentence transformer")
            except Exception as e:
                logger.warning(f"Could not load sentence transformer: {e}")
                self.model = None
        else:
            logger.warning("⚠️ Response Evaluator using fallback heuristics")
    
    
    def evaluate_response(
        self,
        response: str,
        question: str,
        skill: str,
        expected_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a candidate's response comprehensively.
        
        Scoring dimensions:
        - Relevance: How well does the response answer the question?
        - Depth: How detailed and specific is the response?
        - Clarity: How well-structured and clear is the response?
        - Confidence: How confident does the candidate sound?
        
        Args:
            response: The candidate's response text
            question: The assessment question asked
            skill: The skill being assessed
            expected_keywords: Optional list of keywords we expect to see
            
        Returns:
            Dict with scores for different dimensions:
            {
                "overall_quality": 0.0-1.0,
                "relevance": 0.0-1.0,
                "depth": 0.0-1.0,
                "clarity": 0.0-1.0,
                "confidence": 0.0-1.0,
                "evidence_tags": ["specific", "example", "project"],
                "proficiency_level": 1-5
            }
            
        Example:
            >>> evaluator = ResponseEvaluator()
            >>> scores = evaluator.evaluate_response(
            ...     response="I used Python for 3 years building data pipelines with Pandas...",
            ...     question="Tell us about your Python experience",
            ...     skill="Python"
            ... )
            >>> print(scores["overall_quality"])  # 0.85
        """
        if not response or len(response.strip()) < 5:
            return self._null_response_scores()
        
        # Calculate individual scores
        relevance_score = self._score_relevance(response, question)
        depth_score = self._score_depth(response, expected_keywords)
        clarity_score = self._score_clarity(response)
        confidence_score = self._score_confidence(response)
        
        # Extract evidence tags
        evidence_tags = self._extract_evidence_tags(response)
        
        # Calculate overall quality
        overall_quality = (
            relevance_score * 0.30 +
            depth_score * 0.35 +
            clarity_score * 0.20 +
            confidence_score * 0.15
        )
        
        # Map quality score to proficiency level (1-5)
        proficiency_level = self._score_to_proficiency_level(overall_quality)
        
        return {
            "overall_quality": round(overall_quality, 2),
            "relevance": round(relevance_score, 2),
            "depth": round(depth_score, 2),
            "clarity": round(clarity_score, 2),
            "confidence": round(confidence_score, 2),
            "evidence_tags": evidence_tags,
            "proficiency_level": proficiency_level
        }
    
    
    def _score_relevance(self, response: str, question: str) -> float:
        """
        Score how well the response answers the question.
        
        Uses semantic similarity if model available, else heuristics.
        
        Args:
            response: Candidate's response
            question: The question asked
            
        Returns:
            Relevance score 0-1
        """
        if not question:
            return 0.5
        
        # If we have the transformer model, use semantic similarity
        if self.model:
            try:
                q_embedding = self.model.encode(question, convert_to_tensor=True)
                r_embedding = self.model.encode(response, convert_to_tensor=True)
                similarity = util.pytorch_cos_sim(q_embedding, r_embedding).item()
                return min(similarity, 1.0)
            except Exception as e:
                logger.debug(f"Semantic similarity calculation failed: {e}")
        
        # Fallback heuristic: check for keyword overlap
        q_words = set(question.lower().split())
        r_words = set(response.lower().split())
        
        if not q_words:
            return 0.5
        
        overlap = len(q_words & r_words) / len(q_words)
        return min(overlap, 1.0)
    
    
    def _score_depth(self, response: str, expected_keywords: Optional[List[str]] = None) -> float:
        """
        Score the depth and specificity of the response.
        
        Args:
            response: The response text
            expected_keywords: Keywords that indicate depth
            
        Returns:
            Depth score 0-1
        """
        response_lower = response.lower()
        depth_score = 0.0
        
        # Length indicator
        word_count = len(response.split())
        if word_count < 20:
            depth_score = 0.2
        elif word_count < 50:
            depth_score = 0.4
        elif word_count < 150:
            depth_score = 0.6
        else:
            depth_score = 0.8
        
        # Specificity indicators (from quality_keywords)
        for indicator in self.quality_keywords["high"]:
            if indicator in response_lower:
                depth_score += 0.1
        
        # Expected keywords
        if expected_keywords:
            for keyword in expected_keywords:
                if keyword.lower() in response_lower:
                    depth_score += 0.05
        
        return min(depth_score, 1.0)
    
    
    def _score_clarity(self, response: str) -> float:
        """
        Score the clarity and structure of the response.
        
        Args:
            response: The response text
            
        Returns:
            Clarity score 0-1
        """
        clarity_score = 0.7  # Default moderate clarity
        response_lower = response.lower()
        
        # Sentence count (more structured = better)
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        if len(sentences) < 2:
            clarity_score -= 0.2
        elif len(sentences) > 5:
            clarity_score += 0.1
        
        # Check for low-clarity phrases
        for phrase in self.quality_keywords["low"]:
            if phrase in response_lower:
                clarity_score -= 0.05
        
        # Check for structured language
        structure_phrases = ["first", "second", "furthermore", "however", "therefore", "in conclusion"]
        for phrase in structure_phrases:
            if phrase in response_lower:
                clarity_score += 0.05
        
        return min(max(clarity_score, 0.0), 1.0)
    
    
    def _score_confidence(self, response: str) -> float:
        """
        Score the confidence level evident in the response.
        
        Args:
            response: The response text
            
        Returns:
            Confidence score 0-1
        """
        response_lower = response.lower()
        confidence_score = 0.5
        
        # High confidence indicators
        confident_phrases = [
            "i am confident", "i have successfully", "i implemented", 
            "i designed", "i led", "i achieved", "i solved", "i built",
            "we successfully", "our team achieved"
        ]
        
        for phrase in confident_phrases:
            if phrase in response_lower:
                confidence_score += 0.1
        
        # Low confidence indicators
        uncertain_phrases = [
            "i'm not sure", "i don't know", "i think maybe", 
            "probably", "possibly", "perhaps", "kind of", "sort of"
        ]
        
        for phrase in uncertain_phrases:
            if phrase in response_lower:
                confidence_score -= 0.1
        
        # Use of specific examples and numbers boosts confidence
        if any(char.isdigit() for char in response):
            confidence_score += 0.1
        
        return min(max(confidence_score, 0.0), 1.0)
    
    
    def _extract_evidence_tags(self, response: str) -> List[str]:
        """
        Extract evidence tags that support the candidate's claim.
        
        Args:
            response: The response text
            
        Returns:
            List of evidence tags
        """
        tags = []
        response_lower = response.lower()
        
        tag_keywords = {
            "specific": ["specifically", "in particular", "for instance", "for example"],
            "project": ["project", "work", "system", "application", "product"],
            "experience": ["years", "experience", "worked", "implemented", "built"],
            "metrics": ["improved", "increased", "reduced", "achieved", "%", "percent"],
            "technical": ["code", "architecture", "algorithm", "optimization", "performance"],
            "team": ["team", "collaborated", "worked with", "led", "managed"],
            "learning": ["learned", "studied", "learned", "discovered", "understand"]
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in response_lower for kw in keywords):
                tags.append(tag)
        
        return tags
    
    
    def _score_to_proficiency_level(self, score: float) -> int:
        """
        Convert quality score to proficiency level (1-5).
        
        Args:
            score: Quality score 0-1
            
        Returns:
            Proficiency level 1-5
        """
        if score < 0.2:
            return 1  # Beginner
        elif score < 0.4:
            return 2  # Elementary
        elif score < 0.6:
            return 3  # Intermediate
        elif score < 0.8:
            return 4  # Advanced
        else:
            return 5  # Expert
    
    
    def _null_response_scores(self) -> Dict[str, Any]:
        """Get zero/default scores for empty or invalid responses."""
        return {
            "overall_quality": 0.1,
            "relevance": 0.0,
            "depth": 0.0,
            "clarity": 0.0,
            "confidence": 0.0,
            "evidence_tags": [],
            "proficiency_level": 1
        }
    
    
    def compare_responses(
        self,
        response1: str,
        response2: str,
        question: str
    ) -> Dict[str, Any]:
        """
        Compare two responses for the same question.
        
        Args:
            response1: First candidate response
            response2: Second candidate response
            question: The question asked
            
        Returns:
            Comparison results with winner
        """
        scores1 = self.evaluate_response(response1, question, "")
        scores2 = self.evaluate_response(response2, question, "")
        
        overall1 = scores1["overall_quality"]
        overall2 = scores2["overall_quality"]
        
        return {
            "response1_quality": overall1,
            "response2_quality": overall2,
            "better_response": 1 if overall1 > overall2 else (2 if overall2 > overall1 else 0),
            "quality_difference": abs(overall1 - overall2),
            "scores1": scores1,
            "scores2": scores2
        }


# Module-level convenience function

_evaluator = None

def evaluate_response_quality(
    response: str,
    question: str,
    skill: str,
    expected_keywords: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Evaluate response quality using the default evaluator.
    
    Convenience function for use in agents and endpoints.
    
    Args:
        response: The candidate's response
        question: The question that was asked
        skill: The skill being assessed
        expected_keywords: Optional keywords to look for
        
    Returns:
        Dict with evaluation scores
    """
    global _evaluator
    if _evaluator is None:
        _evaluator = ResponseEvaluator()
    
    return _evaluator.evaluate_response(response, question, skill, expected_keywords)
