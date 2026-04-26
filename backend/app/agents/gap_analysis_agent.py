"""
Gap Analysis Agent - Identifies and ranks skill gaps.

This agent compares assessed proficiency levels against JD requirements
to identify gaps and rank them by severity for learning prioritization.

Features:
- Gap severity classification (critical, high, medium, low)
- JD readiness percentage calculation
- Upskilling path creation for each gap
- Strength identification (zero-gap skills)
- Skill combination suggestions for accelerated learning
"""

from typing import List, Dict, Optional
from loguru import logger

from app.schemas import SkillScore


class GapAnalysisResult:
    """Result of gap analysis."""
    
    def __init__(self, session_id: str):
        """Initialize gap analysis result."""
        self.session_id = session_id
        self.critical_gaps: List[Dict] = []
        self.high_gaps: List[Dict] = []
        self.medium_gaps: List[Dict] = []
        self.low_gaps: List[Dict] = []
        self.strengths: List[str] = []
        self.overall_readiness: float = 0.0
        self.recommended_focus: List[str] = []


class GapAnalysisAgent:
    """Analyzes skill gaps between assessment and JD requirements."""
    
    def __init__(self):
        """Initialize the Gap Analysis Agent."""
        logger.info("🔍 Gap Analysis Agent initialized")
    
    
    async def analyze_skill_gaps(
        self,
        skill_scores: List[SkillScore],
        jd_skills: List[str],
        max_level: int = 5
    ) -> GapAnalysisResult:
        """
        Analyze skill gaps and create development priorities.
        
        Gap Severity:
        - Critical: gap >= 3 (missing fundamental capability)
        - High: gap = 2 (significant improvement needed)
        - Medium: gap = 1 (refinement needed)
        - Low: gap = 0 (already proficient)
        
        Args:
            skill_scores: List of assessed skill scores
            jd_skills: List of skills required by JD
            max_level: Maximum proficiency level
            
        Returns:
            GapAnalysisResult with categorized gaps and readiness score
            
        Example:
            >>> result = await agent.analyze_skill_gaps(
            ...     skill_scores=[...],
            ...     jd_skills=["Python", "AWS", "Docker"]
            ... )
            >>> print(f"Overall readiness: {result.overall_readiness:.1%}")
            >>> print(f"Critical gaps: {len(result.critical_gaps)}")
        """
        
        try:
            result = GapAnalysisResult(session_id="session")
            
            # Calculate total possible proficiency
            total_required_proficiency = sum(s.jd_required_level for s in skill_scores)
            total_assessed_proficiency = sum(s.assessed_level for s in skill_scores)
            
            # Calculate overall readiness
            if total_required_proficiency > 0:
                result.overall_readiness = total_assessed_proficiency / total_required_proficiency
            
            # Categorize gaps
            for skill_score in skill_scores:
                gap = skill_score.gap
                
                if gap == 0:
                    # Strength - already proficient
                    result.strengths.append(skill_score.skill)
                    logger.info(f"✅ Strength: {skill_score.skill} (Level {skill_score.assessed_level})")
                
                elif gap >= 3:
                    # Critical gap
                    result.critical_gaps.append({
                        'skill': skill_score.skill,
                        'current_level': skill_score.assessed_level,
                        'required_level': skill_score.jd_required_level,
                        'gap': gap,
                        'priority': 'CRITICAL',
                        'estimated_weeks': 4 + (gap - 3) * 2,
                        'reasoning': self._gap_reasoning(skill_score, 'critical')
                    })
                    logger.warning(f"🔴 Critical gap: {skill_score.skill} (gap: {gap})")
                
                elif gap == 2:
                    # High gap
                    result.high_gaps.append({
                        'skill': skill_score.skill,
                        'current_level': skill_score.assessed_level,
                        'required_level': skill_score.jd_required_level,
                        'gap': gap,
                        'priority': 'HIGH',
                        'estimated_weeks': 2 + (gap - 1) * 2,
                        'reasoning': self._gap_reasoning(skill_score, 'high')
                    })
                    logger.warning(f"🟠 High gap: {skill_score.skill} (gap: {gap})")
                
                elif gap == 1:
                    # Medium gap
                    result.medium_gaps.append({
                        'skill': skill_score.skill,
                        'current_level': skill_score.assessed_level,
                        'required_level': skill_score.jd_required_level,
                        'gap': gap,
                        'priority': 'MEDIUM',
                        'estimated_weeks': 1.5,
                        'reasoning': self._gap_reasoning(skill_score, 'medium')
                    })
                    logger.info(f"🟡 Medium gap: {skill_score.skill} (gap: {gap})")
            
            # Identify missing skills (in JD but not assessed)
            assessed_skills = {s.skill for s in skill_scores}
            missing_skills = set(jd_skills) - assessed_skills
            
            if missing_skills:
                logger.warning(f"⚠️ Skills not assessed: {', '.join(missing_skills)}")
            
            # Create recommended focus areas
            result.recommended_focus = self._create_recommended_focus(
                result.critical_gaps + result.high_gaps + result.medium_gaps,
                result.strengths
            )
            
            logger.info(f"📊 Gap Analysis Complete: {result.overall_readiness:.1%} readiness")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error analyzing gaps: {str(e)}")
            return GapAnalysisResult(session_id="session")
    
    
    def _gap_reasoning(self, skill_score: SkillScore, severity: str) -> str:
        """
        Generate human-readable reasoning for the gap.
        
        Args:
            skill_score: The skill score with gap information
            severity: Gap severity level
            
        Returns:
            Reasoning string
        """
        gap_reasons = {
            'critical': f"Missing foundational knowledge in {skill_score.skill}. "
                       f"Current: Level {skill_score.assessed_level}, "
                       f"Required: Level {skill_score.jd_required_level}. "
                       f"Recommend focused learning program.",
            
            'high': f"Significant improvement needed in {skill_score.skill}. "
                   f"Current: Level {skill_score.assessed_level}, "
                   f"Required: Level {skill_score.jd_required_level}. "
                   f"Recommend structured practice.",
            
            'medium': f"Some refinement needed in {skill_score.skill}. "
                     f"Current: Level {skill_score.assessed_level}, "
                     f"Required: Level {skill_score.jd_required_level}. "
                     f"Recommend practice and review."
        }
        
        return gap_reasons.get(severity, "Gap identified for skill improvement")
    
    
    def _create_recommended_focus(
        self,
        gaps: List[Dict],
        strengths: List[str]
    ) -> List[str]:
        """
        Create recommended focus areas based on gaps and strengths.
        
        Args:
            gaps: List of gap dictionaries (all levels combined)
            strengths: List of strength skill names
            
        Returns:
            List of recommended focus areas
        """
        recommendations = []
        
        # Sort gaps by priority
        critical_skills = [g['skill'] for g in gaps if g['priority'] == 'CRITICAL']
        high_skills = [g['skill'] for g in gaps if g['priority'] == 'HIGH']
        
        if critical_skills:
            recommendations.append(
                f"🔴 URGENT: Master {critical_skills[0]} first "
                f"(foundational for {len(critical_skills)} critical gap(s))"
            )
        
        if high_skills:
            recommendations.append(
                f"🟠 HIGH PRIORITY: Improve {high_skills[0]} and related areas "
                f"({len(high_skills)} high-priority skill(s))"
            )
        
        if strengths:
            recommendations.append(
                f"✅ LEVERAGE: Build on your {strengths[0]} expertise "
                f"(strong in {len(strengths)} skill(s))"
            )
        
        return recommendations[:3]  # Top 3 recommendations
    
    
    def calculate_readiness_score(
        self,
        skill_scores: List[SkillScore]
    ) -> Dict:
        """
        Calculate detailed readiness metrics.
        
        Args:
            skill_scores: List of assessed skill scores
            
        Returns:
            Dictionary with readiness metrics
        """
        if not skill_scores:
            return {
                'overall': 0.0,
                'coverage': 0.0,
                'confidence': 0.0,
                'timeline_weeks': 0
            }
        
        # Overall readiness
        total_required = sum(s.jd_required_level for s in skill_scores)
        total_assessed = sum(s.assessed_level for s in skill_scores)
        overall = total_assessed / total_required if total_required > 0 else 0
        
        # Coverage (skills with some proficiency)
        covered = sum(1 for s in skill_scores if s.assessed_level > 0)
        coverage = covered / len(skill_scores) if skill_scores else 0
        
        # Average confidence
        avg_confidence = sum(s.confidence for s in skill_scores) / len(skill_scores) if skill_scores else 0
        
        # Estimated timeline
        total_gap = sum(max(0, s.gap) for s in skill_scores)
        estimated_weeks = max(1, total_gap * 1.5)  # 1.5 weeks per gap level
        
        return {
            'overall': min(1.0, overall),
            'coverage': coverage,
            'confidence': avg_confidence,
            'timeline_weeks': estimated_weeks
        }
    
    
    def get_skill_combination_suggestions(
        self,
        skill_scores: List[SkillScore],
        skill_graph: Optional[Dict[str, List[str]]] = None
    ) -> List[str]:
        """
        Suggest skill combinations for accelerated learning.
        
        Skills that complement each other can be learned together
        for faster overall improvement.
        
        Args:
            skill_scores: List of assessed skill scores
            skill_graph: Graph of related skills (e.g., Python + Pandas)
            
        Returns:
            List of skill combination suggestions
        """
        if not skill_graph:
            skill_graph = self._default_skill_graph()
        
        suggestions = []
        gap_skills = [s.skill for s in skill_scores if s.gap > 0]
        
        for skill in gap_skills[:3]:  # Top 3 gap skills
            if skill in skill_graph:
                complementary = skill_graph[skill]
                # Find complementary skills that also have gaps
                related_gaps = [c for c in complementary if c in gap_skills]
                
                if related_gaps:
                    combo = f"{skill} + {', '.join(related_gaps[:2])}"
                    suggestions.append(combo)
        
        return suggestions[:3]  # Top 3 combinations
    
    
    def _default_skill_graph(self) -> Dict[str, List[str]]:
        """Default skill relationships for learning combinations."""
        return {
            'Python': ['Pandas', 'NumPy', 'Django'],
            'AWS': ['Docker', 'Kubernetes', 'Terraform'],
            'Docker': ['Kubernetes', 'AWS', 'CI/CD'],
            'React': ['JavaScript', 'TypeScript', 'Redux'],
            'Machine Learning': ['Python', 'Statistics', 'TensorFlow'],
            'Kubernetes': ['Docker', 'AWS', 'Helm'],
            'Database': ['SQL', 'PostgreSQL', 'MongoDB'],
        }


# Module-level convenience functions

async def analyze_skill_gaps(
    skill_scores: List[SkillScore],
    jd_skills: List[str]
) -> GapAnalysisResult:
    """
    Analyze skill gaps using default agent instance.
    
    Convenience function for backward compatibility.
    """
    agent = GapAnalysisAgent()
    return await agent.analyze_skill_gaps(
        skill_scores=skill_scores,
        jd_skills=jd_skills
    )
