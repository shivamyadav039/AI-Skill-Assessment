"""
Planning Agent - Generates personalized learning plans.

This agent creates detailed learning roadmaps with milestones, objectives,
and resource recommendations to bridge identified skill gaps.

Features:
- SMART objective creation for each skill
- Weekly milestone planning with progression
- Prerequisite tracking and dependencies
- Assessment criteria for milestone completion
- Learning resource recommendations
- Success metrics and KPIs
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger

from app.schemas import SkillScore, LearningPlan, LearningMilestone, ResourceRecommendation


class PlanningAgent:
    """Generates personalized learning plans for skill improvement."""
    
    def __init__(self):
        """Initialize the Planning Agent."""
        logger.info("📚 Planning Agent initialized")
    
    
    async def generate_learning_plan(
        self,
        skill_scores: List[SkillScore],
        jd_skills: List[str],
        available_resources: Optional[List[Dict]] = None,
        start_date: Optional[datetime] = None,
        weekly_hours: float = 20.0
    ) -> LearningPlan:
        """
        Generate a comprehensive learning plan to achieve JD requirements.
        
        Plan Structure:
        - Identify priority skills (gaps >= 1)
        - Create weekly milestones for each priority skill
        - Include prerequisite skills
        - Provide resource recommendations
        - Track success metrics
        
        Args:
            skill_scores: List of assessed skill scores
            jd_skills: List of JD-required skills
            available_resources: List of available learning resources
            start_date: Plan start date (defaults to today)
            weekly_hours: Hours per week available for learning
            
        Returns:
            LearningPlan with milestones, resources, and timelines
            
        Example:
            >>> plan = await agent.generate_learning_plan(
            ...     skill_scores=[...],
            ...     jd_skills=["Python", "AWS"],
            ...     weekly_hours=15
            ... )
            >>> print(f"Total duration: {plan.total_duration_weeks} weeks")
            >>> print(f"Milestones: {len(plan.milestones)}")
        """
        
        try:
            if start_date is None:
                start_date = datetime.utcnow()
            
            # Identify priority skills (those with gaps)
            priority_skills = [s for s in skill_scores if s.gap > 0]
            priority_skills.sort(key=lambda x: x.gap, reverse=True)  # Sort by gap severity
            
            logger.info(f"📋 Creating learning plan with {len(priority_skills)} priority skills")
            
            # Create milestones
            milestones = []
            current_date = start_date
            week_number = 1
            
            for skill_score in priority_skills:
                # Calculate weeks needed for this skill
                weeks_needed = self._estimate_weeks_needed(
                    skill_score.gap,
                    weekly_hours
                )
                
                # Create milestones for this skill
                skill_milestones = self._create_skill_milestones(
                    skill=skill_score.skill,
                    current_level=skill_score.assessed_level,
                    target_level=skill_score.jd_required_level,
                    start_date=current_date,
                    weeks_available=weeks_needed,
                    week_number=week_number
                )
                
                milestones.extend(skill_milestones)
                current_date += timedelta(weeks=weeks_needed + 1)  # +1 week buffer
                week_number += len(skill_milestones)
            
            # Calculate total plan duration
            total_duration = self._calculate_total_duration(milestones)
            
            # Get resources
            resources = self._curate_resources(
                priority_skills,
                available_resources
            )
            
            # Create learning plan
            plan = LearningPlan(
                session_id="session",
                candidate_name="Candidate",
                total_duration_weeks=int(total_duration),
                priority_skills=[s.skill for s in priority_skills[:3]],
                adjacent_skills=self._get_adjacent_skills(priority_skills),
                milestones=milestones,
                success_metrics=self._create_success_metrics(skill_scores),
                created_at=datetime.utcnow()
            )
            
            logger.info(f"✅ Learning plan created: {total_duration} weeks, {len(milestones)} milestones")
            return plan
            
        except Exception as e:
            logger.error(f"❌ Error generating learning plan: {str(e)}")
            # Return default/empty plan
            return self._get_default_plan(start_date or datetime.utcnow())
    
    
    def _estimate_weeks_needed(self, gap: int, weekly_hours: float) -> float:
        """
        Estimate weeks needed to close skill gap.
        
        Args:
            gap: Gap size (1-5)
            weekly_hours: Hours available per week
            
        Returns:
            Estimated weeks needed
            
        Formula: gap * 40 hours / weekly_hours
        - Each gap level = ~40 hours of study/practice
        """
        hours_per_gap_level = 40
        total_hours = gap * hours_per_gap_level
        weeks = total_hours / weekly_hours if weekly_hours > 0 else 4
        
        # Minimum 1 week, maximum based on hours
        return max(1, min(weeks, 12))
    
    
    def _create_skill_milestones(
        self,
        skill: str,
        current_level: int,
        target_level: int,
        start_date: datetime,
        weeks_available: float,
        week_number: int
    ) -> List[LearningMilestone]:
        """
        Create weekly milestones for a skill.
        
        Args:
            skill: Skill name
            current_level: Current proficiency level
            target_level: Target proficiency level
            start_date: Milestone start date
            weeks_available: Weeks to reach target
            week_number: Starting week number in plan
            
        Returns:
            List of learning milestones
        """
        milestones = []
        gap = max(0, target_level - current_level)
        
        if gap == 0:
            return []
        
        # Divide weeks among levels to close
        weeks_per_level = weeks_available / gap if gap > 0 else 1
        
        for level_idx in range(1, gap + 1):
            milestone_date = start_date + timedelta(weeks=weeks_per_level * level_idx)
            target_for_milestone = current_level + level_idx
            
            milestone = LearningMilestone(
                week=week_number + level_idx - 1,
                skill=skill,
                objective=f"Achieve Level {target_for_milestone} proficiency in {skill}",
                resources=[],
                prerequisite_skills=[],
                assessment_criteria=self._create_assessment_criteria(skill, target_for_milestone)
            )
            
            milestones.append(milestone)
            logger.info(f"📍 Milestone: Week {milestone.week} - {milestone.objective}")
        
        return milestones
    
    
    def _create_milestone_description(
        self,
        skill: str,
        target_level: int,
        next_level: int
    ) -> str:
        """Create human-readable milestone description."""
        level_names = {
            1: "Beginner",
            2: "Elementary",
            3: "Intermediate",
            4: "Advanced",
            5: "Expert"
        }
        
        return f"Progress {skill} to {level_names.get(target_level, 'Advanced')} level. " \
               f"Gain practical experience and solve real-world problems."
    
    
    def _create_assessment_criteria(self, skill: str, level: int) -> List[str]:
        """Create assessment criteria for milestone completion."""
        criteria = [
            f"Can explain 5+ core concepts of {skill} at this level",
            f"Solved 3+ practice problems successfully",
            f"Completed 1 hands-on project demonstrating competency",
            f"Can teach basic concepts to someone at previous level",
            f"Achieved 80%+ accuracy on self-assessment quiz"
        ]
        
        if level >= 3:
            criteria.append(f"Contributed to open-source project using {skill}")
        
        if level >= 4:
            criteria.append(f"Mentored someone in {skill} or led a discussion")
        
        return criteria[:4]  # Top 4 criteria
    
    
    def _get_difficulty_label(self, level_idx: int, total_gap: int) -> str:
        """Get difficulty label for milestone."""
        if level_idx <= total_gap * 0.33:
            return "Beginner"
        elif level_idx <= total_gap * 0.66:
            return "Intermediate"
        else:
            return "Advanced"
    
    
    def _calculate_total_duration(self, milestones: List[LearningMilestone]) -> float:
        """Calculate total plan duration from milestones."""
        if not milestones:
            return 0
        
        # Get max week number and add 1 for duration
        return max(m.week for m in milestones) + 1
    
    
    def _create_plan_objective(self, priority_skills: List[SkillScore]) -> str:
        """Create main objective for the learning plan."""
        if not priority_skills:
            return "Continuous professional development"
        
        top_skills = [s.skill for s in priority_skills[:3]]
        return f"Achieve proficiency in {', '.join(top_skills)} " \
               f"to meet job requirements within 8-12 weeks"
    
    
    def _get_adjacent_skills(self, priority_skills: List[SkillScore]) -> List[str]:
        """Get adjacent/related skills to build on existing knowledge."""
        skill_graph = {
            "Python": ["Pandas", "NumPy", "Django"],
            "AWS": ["Docker", "Kubernetes", "Terraform"],
            "Docker": ["Kubernetes", "AWS", "CI/CD"],
            "React": ["JavaScript", "TypeScript", "Redux"],
            "Machine Learning": ["Python", "Statistics", "TensorFlow"],
            "Kubernetes": ["Docker", "AWS", "Helm"],
            "Database": ["SQL", "PostgreSQL", "MongoDB"],
        }
        
        adjacent = []
        for skill_score in priority_skills[:2]:  # Top 2 skills
            skill = skill_score.skill
            if skill in skill_graph:
                adjacent.extend(skill_graph[skill][:2])
        
        return list(set(adjacent))[:3]  # Remove duplicates, return top 3
    
    
    def _curate_resources(
        self,
        priority_skills: List[SkillScore],
        available_resources: Optional[List[Dict]] = None
    ) -> List[ResourceRecommendation]:
        """
        Curate learning resources for priority skills.
        
        TODO: Integrate with RAG service for real resource recommendations
        For MVP, returns template resources
        
        Args:
            priority_skills: Skills to find resources for
            available_resources: Pre-provided resources
            
        Returns:
            List of recommended resources
        """
        resources = []
        
        # Default resource recommendations
        for skill_score in priority_skills[:3]:
            skill = skill_score.skill
            
            # Create 2-3 resources per skill
            resources.append(ResourceRecommendation(
                title=f"{skill} Fundamentals Course",
                url=f"https://learn.example.com/{skill.lower()}-basics",
                type="online_course",
                difficulty="Beginner",
                estimated_hours=20,
                rating=4.5,
                price=0  # Free
            ))
            
            resources.append(ResourceRecommendation(
                title=f"Advanced {skill} Patterns",
                url=f"https://learn.example.com/{skill.lower()}-advanced",
                type="online_course",
                difficulty="Intermediate",
                estimated_hours=15,
                rating=4.7,
                price=29
            ))
            
            if skill_score.gap >= 2:
                resources.append(ResourceRecommendation(
                    title=f"{skill} Project-Based Learning",
                    url=f"https://projects.example.com/{skill.lower()}",
                    type="project",
                    difficulty="Advanced",
                    estimated_hours=30,
                    rating=4.6,
                    price=0
                ))
        
        logger.info(f"📚 Curated {len(resources)} learning resources")
        return resources
    
    
    def _create_success_metrics(self, skill_scores: List[SkillScore]) -> Dict[str, float]:
        """Create success metrics and KPIs for the plan."""
        return {
            'target_readiness': 0.85,  # 85% readiness by end of plan
            'milestone_completion': 1.0,  # 100% milestone completion
            'skill_improvement': min(1.0, sum(s.gap for s in skill_scores) * 0.1),
            'assessment_score_improvement': 0.3,  # Improve by 30%
        }
    
    
    def _calculate_plan_confidence(self, skill_scores: List[SkillScore]) -> float:
        """Calculate confidence in the learning plan."""
        if not skill_scores:
            return 0.5
        
        # Average confidence of assessed skills
        avg_confidence = sum(s.confidence for s in skill_scores) / len(skill_scores)
        
        # Higher confidence = better plan based on more reliable assessments
        return min(1.0, avg_confidence * 1.1)
    
    
    def _get_default_plan(self, start_date: datetime) -> LearningPlan:
        """Return default/minimal learning plan."""
        return LearningPlan(
            session_id="session",
            candidate_name="Candidate",
            total_duration_weeks=0,
            priority_skills=[],
            adjacent_skills=[],
            milestones=[],
            success_metrics={},
            created_at=datetime.utcnow()
        )


# Module-level convenience functions

async def generate_learning_plan(
    skill_scores: List[SkillScore],
    jd_skills: List[str],
    available_resources: Optional[List[Dict]] = None
) -> LearningPlan:
    """
    Generate learning plan using default agent instance.
    
    Convenience function for backward compatibility.
    """
    agent = PlanningAgent()
    return await agent.generate_learning_plan(
        skill_scores=skill_scores,
        jd_skills=jd_skills,
        available_resources=available_resources
    )
