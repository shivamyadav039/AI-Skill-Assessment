"""
Planning Agent - Generates personalized AI-powered learning plans.

Uses NVIDIA NIM LLM to create rich, actionable learning roadmaps with real
resource recommendations tailored to each candidate's skill gaps.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger

from app.schemas import SkillScore, LearningPlan, LearningMilestone, ResourceRecommendation


class PlanningAgent:
    """Generates personalized learning plans powered by NVIDIA NIM."""

    def __init__(self):
        logger.info("📚 Planning Agent initialized")

    # ------------------------------------------------------------------ main

    async def generate_learning_plan(
        self,
        skill_scores: List[SkillScore],
        jd_skills: List[str],
        candidate_name: str = "Candidate",
        available_resources: Optional[List[Dict]] = None,
        start_date: Optional[datetime] = None,
        weekly_hours: float = 20.0,
    ) -> LearningPlan:
        """
        Generate a comprehensive, LLM-powered learning plan.

        Args:
            skill_scores: Assessed skill scores
            jd_skills: JD-required skills
            candidate_name: Candidate's name
            available_resources: Optional pre-provided resources
            start_date: Plan start date (defaults to today)
            weekly_hours: Hours per week available for learning

        Returns:
            LearningPlan with AI-generated milestones and resources
        """
        try:
            if start_date is None:
                start_date = datetime.utcnow()

            # Sort by gap descending — most critical first
            priority_scores = sorted(
                [s for s in skill_scores if s.gap > 0],
                key=lambda x: x.gap,
                reverse=True,
            )

            logger.info(f"📋 Generating AI plan for {len(priority_scores)} priority skills")

            milestones: List[LearningMilestone] = []
            week_number = 1
            current_date = start_date

            for skill_score in priority_scores[:5]:  # Cap at 5 priority skills
                weeks_needed = self._estimate_weeks_needed(skill_score.gap, weekly_hours)

                skill_milestones = await self._generate_ai_milestones(
                    skill=skill_score.skill,
                    current_level=skill_score.assessed_level,
                    target_level=skill_score.jd_required_level,
                    start_date=current_date,
                    weeks_available=int(weeks_needed),
                    week_number=week_number,
                )

                milestones.extend(skill_milestones)
                current_date += timedelta(weeks=int(weeks_needed) + 1)
                week_number += len(skill_milestones)

            total_duration = max(m.week for m in milestones) + 1 if milestones else 0

            plan = LearningPlan(
                session_id="session",
                candidate_name=candidate_name,
                total_duration_weeks=int(total_duration),
                priority_skills=[s.skill for s in priority_scores[:3]],
                adjacent_skills=self._get_adjacent_skills(priority_scores),
                milestones=milestones,
                success_metrics=self._create_success_metrics(skill_scores),
                created_at=datetime.utcnow(),
            )

            logger.info(f"✅ Plan created: {total_duration} weeks, {len(milestones)} milestones")
            return plan

        except Exception as e:
            logger.error(f"❌ Error generating learning plan: {e}")
            return self._get_default_plan(start_date or datetime.utcnow(), candidate_name)

    # -------------------------------------------------------- AI milestone gen

    async def _generate_ai_milestones(
        self,
        skill: str,
        current_level: int,
        target_level: int,
        start_date: datetime,
        weeks_available: int,
        week_number: int,
    ) -> List[LearningMilestone]:
        """Use NVIDIA NIM to generate rich, contextual milestones for a skill."""
        gap = max(0, target_level - current_level)
        if gap == 0:
            return []

        level_names = {1: "Beginner", 2: "Elementary", 3: "Intermediate", 4: "Advanced", 5: "Expert"}
        current_name = level_names.get(current_level, "Unknown")
        target_name = level_names.get(target_level, "Unknown")

        system_prompt = f"""You are an expert learning plan designer for software engineers.
Your job is to create precise, actionable week-by-week learning milestones.
Always respond with ONLY valid JSON — no markdown, no explanation text."""

        user_prompt = f"""Create a {weeks_available}-week learning plan to take a developer from {current_name} (Level {current_level}) to {target_name} (Level {target_level}) in {skill}.

Generate exactly {gap} milestone(s) as a JSON array. Each milestone must have:
- "week": integer (starting at {week_number})
- "objective": one clear, specific sentence describing the learning goal
- "resources": array of 2-3 objects, each with "title" (string), "type" (string: "course"/"book"/"project"/"practice"), "hours" (int)
- "criteria": array of 2 specific, measurable success criteria strings

Respond with ONLY the JSON array. Example format:
[{{"week": 1, "objective": "...", "resources": [{{"title": "...", "type": "course", "hours": 10}}], "criteria": ["...","..."]}}]"""

        try:
            from app.services import call_claude
            import json

            raw = call_claude(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=800,
                temperature=0.4,
                use_cache=False,
                retry_count=2,
            )

            # Try to parse JSON from response
            raw = raw.strip()
            # Extract JSON array if wrapped in markdown
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            # Find the JSON array
            start = raw.find("[")
            end = raw.rfind("]") + 1
            if start >= 0 and end > start:
                raw = raw[start:end]

            data = json.loads(raw)
            milestones = []

            for i, item in enumerate(data[:gap]):
                resources = []
                for r in item.get("resources", [])[:3]:
                    resources.append(ResourceRecommendation(
                        title=r.get("title", f"{skill} Resource {i+1}"),
                        description=f"Learn {skill} through this {r.get('type', 'resource')}",
                        url=f"https://search.example.com/learn/{skill.lower().replace(' ', '-')}",
                        resource_type=r.get("type", "course"),
                        estimated_duration_hours=int(r.get("hours", 10)),
                        difficulty_level=level_names.get(current_level + i + 1, "intermediate").lower(),
                        relevance_score=0.9,
                    ))

                milestone = LearningMilestone(
                    week=int(item.get("week", week_number + i)),
                    skill=skill,
                    objective=item.get("objective", f"Achieve Level {current_level + i + 1} in {skill}"),
                    resources=resources,
                    prerequisite_skills=[],
                    assessment_criteria=item.get("criteria", [
                        f"Can explain core {skill} concepts at this level",
                        "Completed at least one hands-on project",
                    ]),
                )
                milestones.append(milestone)
                logger.info(f"📍 AI Milestone: Week {milestone.week} — {skill} → {milestone.objective[:60]}...")

            return milestones

        except Exception as e:
            logger.warning(f"AI milestone generation failed for {skill}, using templates: {e}")
            return self._create_template_milestones(
                skill, current_level, target_level, start_date, weeks_available, week_number
            )

    # -------------------------------------------------------- template fallback

    def _create_template_milestones(
        self,
        skill: str,
        current_level: int,
        target_level: int,
        start_date: datetime,
        weeks_available: int,
        week_number: int,
    ) -> List[LearningMilestone]:
        gap = max(0, target_level - current_level)
        level_names = {1: "Beginner", 2: "Elementary", 3: "Intermediate", 4: "Advanced", 5: "Expert"}
        milestones = []
        weeks_per_level = max(1, weeks_available // gap) if gap else 1

        for level_idx in range(1, gap + 1):
            target_for_milestone = current_level + level_idx
            target_name = level_names.get(target_for_milestone, "Advanced")

            resources = [
                ResourceRecommendation(
                    title=f"{skill} {target_name} Course",
                    description=f"Structured course to reach {target_name} level in {skill}",
                    url=f"https://learn.example.com/{skill.lower().replace(' ', '-')}-{target_name.lower()}",
                    resource_type="course",
                    estimated_duration_hours=20,
                    difficulty_level=target_name.lower(),
                    relevance_score=0.85,
                ),
                ResourceRecommendation(
                    title=f"Build a {skill} Project",
                    description=f"Hands-on project to solidify {skill} skills",
                    url=f"https://projects.example.com/{skill.lower().replace(' ', '-')}",
                    resource_type="project",
                    estimated_duration_hours=15,
                    difficulty_level=target_name.lower(),
                    relevance_score=0.90,
                ),
            ]

            milestone = LearningMilestone(
                week=week_number + level_idx - 1,
                skill=skill,
                objective=f"Achieve {target_name} (Level {target_for_milestone}) proficiency in {skill}",
                resources=resources,
                prerequisite_skills=[],
                assessment_criteria=[
                    f"Can solve 3+ real-world {skill} problems independently",
                    f"Completed a project demonstrating Level {target_for_milestone} competency",
                    f"Can explain key {skill} concepts to a peer",
                ],
            )
            milestones.append(milestone)

        return milestones

    # -------------------------------------------------------- helpers

    def _estimate_weeks_needed(self, gap: int, weekly_hours: float) -> float:
        hours_per_gap_level = 40
        total_hours = gap * hours_per_gap_level
        weeks = total_hours / weekly_hours if weekly_hours > 0 else 4
        return max(gap, min(weeks, 12))

    def _get_adjacent_skills(self, priority_skills: List[SkillScore]) -> List[str]:
        skill_graph = {
            "Python": ["Pandas", "NumPy", "Django", "FastAPI"],
            "AWS": ["Docker", "Kubernetes", "Terraform", "CloudFormation"],
            "Docker": ["Kubernetes", "AWS", "CI/CD", "Helm"],
            "React": ["JavaScript", "TypeScript", "Redux", "Next.js"],
            "Machine Learning": ["Python", "Statistics", "TensorFlow", "PyTorch"],
            "Kubernetes": ["Docker", "AWS", "Helm", "Service Mesh"],
            "PostgreSQL": ["SQL", "Redis", "Database Design", "pgvector"],
            "FastAPI": ["Python", "REST API", "Pydantic", "Async Python"],
            "System Design": ["Database Design", "API Design", "Scalability", "Microservices"],
        }
        adjacent = []
        for skill_score in priority_skills[:2]:
            if skill_score.skill in skill_graph:
                adjacent.extend(skill_graph[skill_score.skill][:2])
        return list(dict.fromkeys(adjacent))[:4]

    def _create_success_metrics(self, skill_scores: List[SkillScore]) -> Dict:
        total_gap = sum(max(0, s.gap) for s in skill_scores)
        return {
            "target_readiness": "85%",
            "milestone_completion": "100%",
            "estimated_improvement": f"+{min(total_gap * 15, 60)}% proficiency",
            "weekly_commitment_hours": "10-15 hours",
        }

    def _get_default_plan(self, start_date: datetime, candidate_name: str = "Candidate") -> LearningPlan:
        return LearningPlan(
            session_id="session",
            candidate_name=candidate_name,
            total_duration_weeks=0,
            priority_skills=[],
            adjacent_skills=[],
            milestones=[],
            success_metrics={"target_readiness": "85%"},
            created_at=datetime.utcnow(),
        )


# Module-level convenience function
async def generate_learning_plan(
    skill_scores: List[SkillScore],
    jd_skills: List[str],
    candidate_name: str = "Candidate",
) -> LearningPlan:
    agent = PlanningAgent()
    return await agent.generate_learning_plan(
        skill_scores=skill_scores,
        jd_skills=jd_skills,
        candidate_name=candidate_name,
    )
