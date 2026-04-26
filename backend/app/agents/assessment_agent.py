"""
Assessment Agent - Generates adaptive multi-turn assessment questions.

This agent creates contextual, difficulty-progressing questions to assess
candidate proficiency on specific skills required by the Job Description.

Features:
- Adaptive difficulty progression (conceptual → scenario → applied)
- Multi-turn conversation tracking
- Claude AI integration for domain expertise
- Confidence score extraction from responses
- Graceful completion with fallback logic
"""

import os
from typing import List, Optional
from loguru import logger

from app.schemas import ChatMessage


class AssessmentAgent:
    """Generates adaptive assessment questions for skill evaluation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Assessment Agent.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = "claude-3-5-sonnet-20241022"
        logger.info("🤖 Assessment Agent initialized")
    
    
    async def generate_assessment_question(
        self,
        skill: str,
        turn_count: int,
        conversation_history: List[ChatMessage],
        jd_context: str,
        resume_context: str = ""
    ) -> str:
        """
        Generate adaptive assessment question for a skill.
        
        Difficulty progression:
        - Turn 1: Conceptual understanding (basic definition)
        - Turn 2-3: Practical application (real-world scenario)
        - Turn 4-5: Advanced reasoning (edge cases, optimization)
        
        Args:
            skill: Skill to assess (e.g., "Python")
            turn_count: Number of questions asked so far (1-indexed)
            conversation_history: Previous Q&A in this skill assessment
            jd_context: Job description text for context
            resume_context: Resume text to understand candidate background
            
        Returns:
            Assessment question string
            
        Example:
            >>> question = await agent.generate_assessment_question(
            ...     skill="Python",
            ...     turn_count=1,
            ...     conversation_history=[],
            ...     jd_context="Looking for Python expert with ML experience"
            ... )
            >>> print(question)
            "What is the difference between a list and a tuple in Python?
             How does this affect performance in data processing?"
        """
        
        # Determine difficulty level based on turn count
        if turn_count == 1:
            difficulty = "conceptual"
            focus = "basic understanding and fundamentals"
        elif turn_count <= 3:
            difficulty = "practical"
            focus = "real-world application and problem-solving"
        else:
            difficulty = "advanced"
            focus = "edge cases, optimization, and best practices"
        
        # Build conversation context from history
        conversation_context = self._build_conversation_context(conversation_history)
        
        # Create system prompt for Claude
        system_prompt = f"""You are an expert technical interviewer assessing a candidate's {skill} skills.

Job Context: {jd_context}
{f'Candidate Background: {resume_context}' if resume_context else ''}

Your task: Generate a {difficulty} level assessment question about {skill}.

Requirements:
1. Focus on: {focus}
2. Question should be clear and answerable in 2-3 sentences
3. Avoid yes/no questions - require explanation
4. Build on previous discussion if applicable
5. Be fair but thorough in evaluating competency

Generate ONLY the question. No preamble or explanation."""

        user_prompt = f"""Previous conversation on {skill}:
{conversation_context if conversation_context else 'No previous questions yet'}

Generate the next assessment question (difficulty: {difficulty})."""

        try:
            # TODO: Call Claude API with system and user prompts
            # For now, return a placeholder question
            question = await self._call_claude(system_prompt, user_prompt)
            logger.info(f"✅ Generated {difficulty} question for {skill} (turn {turn_count})")
            return question
            
        except Exception as e:
            logger.error(f"❌ Error generating question: {str(e)}")
            return self._get_fallback_question(skill, turn_count)
    
    
    def _build_conversation_context(self, history: List[ChatMessage]) -> str:
        """
        Build formatted conversation context from chat history.
        
        Args:
            history: List of previous chat messages
            
        Returns:
            Formatted conversation string
        """
        if not history:
            return ""
        
        context_lines = []
        for msg in history[-4:]:  # Last 4 messages for context
            role = "Q:" if msg.role == "assistant" else "A:"
            context_lines.append(f"{role} {msg.content[:200]}...")  # Truncate long messages
        
        return "\n".join(context_lines)
    
    
    async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call Claude API with retry logic.
        
        Phase 3: Uses real LLMService with caching, retries, and fallback.
        
        Args:
            system_prompt: System instruction for Claude
            user_prompt: User message/question
            
        Returns:
            Claude's response
        """
        try:
            from app.services import call_claude
            
            response = call_claude(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=500,
                temperature=0.7,
                use_cache=True
            )
            logger.info(f"✅ Claude API call succeeded")
            return response
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise
    
    
    def _get_fallback_question(self, skill: str, turn_count: int) -> str:
        """
        Get fallback question if API call fails.
        
        Args:
            skill: Skill to assess
            turn_count: Question number
            
        Returns:
            Fallback question string
        """
        fallback_questions = {
            1: f"Can you describe your experience with {skill}? What was your first exposure to it?",
            2: f"Tell us about a project where you used {skill}. What was your role and what did you achieve?",
            3: f"What are some common challenges you've faced with {skill}? How did you overcome them?",
            4: f"How do you stay updated with the latest trends and best practices in {skill}?",
            5: f"If you had to mentor someone in {skill}, what are the top 3 things you'd teach them?"
        }
        
        return fallback_questions.get(turn_count, fallback_questions[5])
    
    
    def should_continue_assessment(
        self,
        turn_count: int,
        response_quality: float,
        max_turns: int = 5
    ) -> bool:
        """
        Determine if assessment should continue or conclude for this skill.
        
        Args:
            turn_count: Number of questions asked
            response_quality: Quality score of last response (0-1)
            max_turns: Maximum questions per skill
            
        Returns:
            True if should ask another question, False if assessment complete
            
        Logic:
            - Stop if max_turns reached
            - Stop if we have high confidence (quality > 0.8 for 3+ turns)
            - Continue otherwise
        """
        if turn_count >= max_turns:
            logger.info(f"Assessment complete (reached max {max_turns} turns)")
            return False
        
        if turn_count >= 3 and response_quality > 0.8:
            logger.info(f"Assessment complete (high confidence with quality {response_quality:.2f})")
            return False
        
        return True
    
    
    def extract_response_quality(self, response: str) -> float:
        """
        Extract quality score from candidate response.
        
        Phase 3: Uses real ResponseEvaluator with NLP-based scoring.
        
        Args:
            response: Candidate's text response
            
        Returns:
            Quality score 0-1
            - 0.0-0.3: Low (vague, incomplete)
            - 0.3-0.7: Medium (adequate, some gaps)
            - 0.7-1.0: High (detailed, specific examples)
        """
        try:
            from app.services import evaluate_response_quality
            
            # Use the current skill and last question from context
            scores = evaluate_response_quality(
                response=response,
                question=getattr(self, 'last_question', "Tell us about your experience"),
                skill=getattr(self, 'current_skill', "General"),
                expected_keywords=None
            )
            
            quality_score = scores.get("overall_quality", 0.5)
            logger.debug(f"Response quality evaluated: {quality_score:.2f}")
            return quality_score
            
        except Exception as e:
            logger.warning(f"ResponseEvaluator error, using fallback: {e}")
            # Fallback to simple heuristics
            if not response or len(response) < 20:
                return 0.2
            
            if len(response) < 100:
                return 0.4
            
            # Check for specific indicators of quality
            quality_indicators = [
                "example",
                "specific",
                "project",
                "implemented",
                "experience",
                "learned",
                "solved"
            ]
            
            quality_score = 0.5
            for indicator in quality_indicators:
                if indicator.lower() in response.lower():
                    quality_score += 0.1
            
            return min(quality_score, 1.0)


# Module-level convenience functions

async def generate_assessment_question(
    skill: str,
    turn_count: int,
    conversation_history: List[ChatMessage],
    jd_context: str,
    resume_context: str = ""
) -> str:
    """
    Generate assessment question using default agent instance.
    
    Convenience function for backward compatibility.
    """
    agent = AssessmentAgent()
    return await agent.generate_assessment_question(
        skill=skill,
        turn_count=turn_count,
        conversation_history=conversation_history,
        jd_context=jd_context,
        resume_context=resume_context
    )
