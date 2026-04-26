"""
Scoring Agent - Evaluates candidate proficiency based on assessment responses.

This agent analyzes the full conversation history to determine candidate proficiency
level on each skill, comparing against JD requirements.

Features:
- Chain-of-Thought reasoning for transparent scoring
- Evidence extraction from responses
- Confidence score calculation
- Comparison with JD requirements
- Human-readable score summaries
"""

import os
from typing import List, Optional, Dict
from loguru import logger

from app.schemas import ChatMessage, SkillScore, ProficiencyLevel


class ScoringAgent:
    """Evaluates candidate proficiency based on assessment responses."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Scoring Agent.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = "claude-3-5-sonnet-20241022"
        logger.info("📊 Scoring Agent initialized")
    
    
    async def score_skill_proficiency(
        self,
        skill: str,
        conversation_history: List[ChatMessage],
        jd_required_level: int = 3,
        max_level: int = 5
    ) -> SkillScore:
        """
        Score candidate proficiency on a skill based on conversation.
        
        Proficiency Levels:
        1. Beginner - Basic understanding, theory only
        2. Intermediate - Some practical experience
        3. Proficient - Can solve typical problems independently
        4. Advanced - Can handle complex scenarios, mentor others
        5. Expert - Deep expertise, innovation, architecture decisions
        
        Args:
            skill: Skill being assessed
            conversation_history: Full Q&A conversation for this skill
            jd_required_level: Required proficiency level (1-5)
            max_level: Maximum possible proficiency level
            
        Returns:
            SkillScore with proficiency level, confidence, and evidence
            
        Example:
            >>> score = await agent.score_skill_proficiency(
            ...     skill="Python",
            ...     conversation_history=[...],
            ...     jd_required_level=3
            ... )
            >>> print(score.proficiency_level)
            ProficiencyLevel.PROFICIENT
        """
        
        try:
            # Analyze conversation for proficiency signals
            analysis = self._analyze_conversation(conversation_history, skill)
            
            # Create scoring prompt
            system_prompt = f"""You are an expert technical evaluator scoring {skill} proficiency.

Proficiency Levels (1-5):
1. Beginner - Basic understanding, theory only
2. Intermediate - Some practical experience, can implement basic solutions
3. Proficient - Solid understanding, can solve typical problems independently
4. Advanced - Complex problem solving, can architect solutions, mentor others
5. Expert - Deep expertise, innovation, sets standards

Your task: Score the candidate's proficiency based on their responses."""

            user_prompt = f"""Skill: {skill}
JD Required Level: {jd_required_level}

Conversation Summary:
{analysis['summary']}

Proficiency Indicators:
- Response Depth: {analysis['response_depth']}/5
- Technical Accuracy: {analysis['technical_accuracy']}/5
- Practical Experience: {analysis['practical_experience']}/5
- Problem-Solving: {analysis['problem_solving']}/5

Based on the conversation above, provide:
1. Proficiency Level (1-5): [NUMBER]
2. Confidence (0-1): [0.XX]
3. Evidence Tags (top 3): [tag1, tag2, tag3]
4. Reasoning (2-3 sentences)

Format your response as:
LEVEL: [number]
CONFIDENCE: [0.xx]
EVIDENCE: [tag1], [tag2], [tag3]
REASONING: [your reasoning]"""

            # Call scoring API
            response = await self._call_claude(system_prompt, user_prompt)
            
            # Parse response
            score_data = self._parse_score_response(response)
            
            # Construct SkillScore object
            skill_score = SkillScore(
                skill=skill,
                assessed_level=score_data['level'],
                confidence=score_data['confidence'],
                evidence_tags=score_data['evidence'],
                jd_required_level=jd_required_level,
                gap=max(0, jd_required_level - score_data['level']),
                conversation_summary=analysis['summary']
            )
            
            logger.info(f"✅ Scored {skill}: Level {score_data['level']}/5 (gap: {skill_score.gap})")
            return skill_score
            
        except Exception as e:
            logger.error(f"❌ Error scoring proficiency: {str(e)}")
            # Return default score
            return self._get_default_score(skill, jd_required_level)
    
    
    def _analyze_conversation(self, history: List[ChatMessage], skill: str) -> Dict:
        """
        Analyze conversation for proficiency indicators.
        
        Phase 3: Uses ResponseEvaluator service for NLP-based analysis.
        
        Args:
            history: Conversation history
            skill: Skill being assessed
            
        Returns:
            Dictionary with analysis metrics
        """
        if not history:
            return {
                'summary': 'No assessment data available',
                'response_depth': 1,
                'technical_accuracy': 1,
                'practical_experience': 1,
                'problem_solving': 1
            }
        
        try:
            from app.services import evaluate_response_quality
            
            # Get candidate responses only (user messages)
            responses = [msg.content for msg in history if msg.role == "user"]
            
            if not responses:
                return {
                    'summary': 'No candidate responses available',
                    'response_depth': 1,
                    'technical_accuracy': 1,
                    'practical_experience': 1,
                    'problem_solving': 1
                }
            
            # Build summary
            summary_lines = []
            for i, response in enumerate(responses, 1):
                if len(response) > 150:
                    summary_lines.append(f"Q{i}: {response[:150]}...")
                else:
                    summary_lines.append(f"Q{i}: {response}")
            
            summary = "\n".join(summary_lines)
            
            # Evaluate responses using NLP service
            avg_depth = 0
            for response in responses:
                scores = evaluate_response_quality(
                    response=response,
                    question=f"Experience with {skill}",
                    skill=skill,
                    expected_keywords=None
                )
                avg_depth += scores.get('depth', 0.5)
            
            avg_depth /= len(responses)
            response_depth = min(5, max(1, int(1 + (avg_depth * 4))))
            
            # Extract evidence-based indicators
            technical_accuracy = self._estimate_technical_accuracy(responses, skill)
            practical_experience = self._estimate_practical_experience(responses)
            problem_solving = self._estimate_problem_solving(responses)
            
            logger.debug(f"Conversation analysis for {skill}: depth={response_depth}")
            
            return {
                'summary': summary,
                'response_depth': response_depth,
                'technical_accuracy': technical_accuracy,
                'practical_experience': practical_experience,
                'problem_solving': problem_solving
            }
            
        except Exception as e:
            logger.warning(f"NLP analysis failed, using heuristics: {e}")
            # Fallback to heuristics
            responses = [msg.content for msg in history if msg.role == "user"]
            
            # Build summary
            summary_lines = []
            for i, response in enumerate(responses, 1):
                if len(response) > 150:
                    summary_lines.append(f"Q{i}: {response[:150]}...")
                else:
                    summary_lines.append(f"Q{i}: {response}")
            
            summary = "\n".join(summary_lines)
            
            # Calculate indicators
            avg_response_length = sum(len(r) for r in responses) / len(responses) if responses else 0
            
            # Simple heuristics for MVP
            response_depth = min(5, max(1, int(avg_response_length / 50)))
            technical_accuracy = self._estimate_technical_accuracy(responses, skill)
            practical_experience = self._estimate_practical_experience(responses)
            problem_solving = self._estimate_problem_solving(responses)
            
            return {
                'summary': summary,
                'response_depth': response_depth,
                'technical_accuracy': technical_accuracy,
                'practical_experience': practical_experience,
                'problem_solving': problem_solving
            }
    
    
    def _estimate_technical_accuracy(self, responses: List[str], skill: str) -> int:
        """Estimate technical accuracy of responses (1-5 scale)."""
        # Check for technical keywords
        technical_keywords = [
            "implementation", "algorithm", "data structure",
            "complexity", "optimization", "scalability",
            "architecture", "pattern", "best practice"
        ]
        
        count = sum(1 for kw in technical_keywords 
                   if any(kw.lower() in r.lower() for r in responses))
        
        return min(5, max(1, 1 + count // 2))
    
    
    def _estimate_practical_experience(self, responses: List[str]) -> int:
        """Estimate practical experience level (1-5 scale)."""
        # Check for experience indicators
        experience_keywords = [
            "project", "implemented", "built", "deployed",
            "production", "real-world", "worked on", "developed"
        ]
        
        count = sum(1 for kw in experience_keywords 
                   if any(kw.lower() in r.lower() for r in responses))
        
        return min(5, max(1, 1 + count // 2))
    
    
    def _estimate_problem_solving(self, responses: List[str]) -> int:
        """Estimate problem-solving ability (1-5 scale)."""
        # Check for problem-solving indicators
        problem_keywords = [
            "solved", "fixed", "debugged", "optimized",
            "challenge", "difficult", "approach", "strategy",
            "trade-off", "alternative"
        ]
        
        count = sum(1 for kw in problem_keywords 
                   if any(kw.lower() in r.lower() for r in responses))
        
        return min(5, max(1, 1 + count // 2))
    
    
    async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call Claude API for scoring.
        
        TODO: Implement actual Claude API call
        For MVP, returns template response
        """
        try:
            # TODO: Uncomment when anthropic client is available
            # import anthropic
            # client = anthropic.Anthropic(api_key=self.api_key)
            # message = client.messages.create(
            #     model=self.model,
            #     max_tokens=500,
            #     system=system_prompt,
            #     messages=[{"role": "user", "content": user_prompt}]
            # )
            # return message.content[0].text
            
            # Placeholder for MVP
            return """LEVEL: 3
CONFIDENCE: 0.85
EVIDENCE: practical-experience, problem-solving, technical-depth
REASONING: Candidate demonstrated solid understanding with real-world project examples."""
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise
    
    
    def _parse_score_response(self, response: str) -> Dict:
        """
        Parse Claude's scoring response.
        
        Args:
            response: Raw response from Claude
            
        Returns:
            Dictionary with extracted score data
        """
        data = {
            'level': 3,
            'confidence': 0.7,
            'evidence': ['experience', 'knowledge', 'potential'],
            'reasoning': 'Adequate proficiency demonstrated'
        }
        
        try:
            lines = response.strip().split('\n')
            for line in lines:
                if line.startswith('LEVEL:'):
                    data['level'] = int(line.split(':')[1].strip())
                elif line.startswith('CONFIDENCE:'):
                    data['confidence'] = float(line.split(':')[1].strip())
                elif line.startswith('EVIDENCE:'):
                    evidence_str = line.split(':')[1].strip()
                    data['evidence'] = [e.strip() for e in evidence_str.split(',')][:3]
                elif line.startswith('REASONING:'):
                    data['reasoning'] = line.split(':')[1].strip()
        except Exception as e:
            logger.warning(f"Could not parse score response: {str(e)}")
        
        return data
    
    
    def _int_to_proficiency_level(self, level: int) -> ProficiencyLevel:
        """Convert numeric level to ProficiencyLevel enum."""
        level_map = {
            1: ProficiencyLevel.BEGINNER,
            2: ProficiencyLevel.ELEMENTARY,
            3: ProficiencyLevel.INTERMEDIATE,
            4: ProficiencyLevel.ADVANCED,
            5: ProficiencyLevel.EXPERT
        }
        return level_map.get(min(5, max(1, level)), ProficiencyLevel.INTERMEDIATE)
    
    
    def _get_default_score(self, skill: str, jd_required_level: int) -> SkillScore:
        """Return default score when scoring fails."""
        return SkillScore(
            skill=skill,
            assessed_level=2,
            confidence=0.5,
            evidence_tags=['insufficient-data'],
            jd_required_level=jd_required_level,
            gap=max(0, jd_required_level - 2),
            conversation_summary='Unable to assess due to technical error'
        )


# Module-level convenience functions

async def score_skill_proficiency(
    skill: str,
    conversation_history: List[ChatMessage],
    jd_required_level: int = 3
) -> SkillScore:
    """
    Score skill proficiency using default agent instance.
    
    Convenience function for backward compatibility.
    """
    agent = ScoringAgent()
    return await agent.score_skill_proficiency(
        skill=skill,
        conversation_history=conversation_history,
        jd_required_level=jd_required_level
    )
