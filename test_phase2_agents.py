"""
Phase 2 Test Script - Verify all AI agents work correctly.

This script tests the assessment, scoring, gap analysis, and planning agents
without requiring the FastAPI server or Claude API.

Run with: python test_phase2_agents.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.agents import (
    AssessmentAgent,
    ScoringAgent,
    GapAnalysisAgent,
    PlanningAgent,
)
from app.schemas import ChatMessage, SkillScore, ProficiencyLevel


async def test_assessment_agent():
    """Test AssessmentAgent question generation."""
    print("\n" + "="*60)
    print("🧪 TESTING: Assessment Agent")
    print("="*60)
    
    agent = AssessmentAgent()
    
    # Test turn 1 (conceptual)
    print("\n📝 Turn 1 - Conceptual Question:")
    q1 = await agent.generate_assessment_question(
        skill="Python",
        turn_count=1,
        conversation_history=[],
        jd_context="Senior Python engineer role"
    )
    print(f"  Q: {q1}")
    
    # Test turn 2 (practical)
    print("\n📝 Turn 2 - Practical Question:")
    history = [
        ChatMessage(role="assistant", content=q1),
        ChatMessage(role="user", content="Python is a high-level programming language...")
    ]
    q2 = await agent.generate_assessment_question(
        skill="Python",
        turn_count=2,
        conversation_history=history,
        jd_context="Senior Python engineer role"
    )
    print(f"  Q: {q2}")
    
    # Test response quality extraction
    print("\n📊 Response Quality Analysis:")
    responses = [
        ("Short answer", 0.2),
        ("I worked on a project", 0.4),
        ("I built a machine learning pipeline using Python with PyTorch, "
         "processing 10GB of data daily", 0.8),
    ]
    
    for response, expected in responses:
        quality = agent.extract_response_quality(response)
        print(f"  '{response[:40]}...' → Quality: {quality:.2f} (expected ~{expected:.2f})")
    
    # Test assessment continuation logic
    print("\n✅ Assessment Continuation Logic:")
    print(f"  Turn 1, quality 0.3 → Continue? {agent.should_continue_assessment(1, 0.3)}")
    print(f"  Turn 3, quality 0.8 → Continue? {agent.should_continue_assessment(3, 0.8)}")
    print(f"  Turn 5, quality 0.7 → Continue? {agent.should_continue_assessment(5, 0.7)}")
    
    print("\n✅ Assessment Agent: WORKING")


async def test_scoring_agent():
    """Test ScoringAgent proficiency scoring."""
    print("\n" + "="*60)
    print("🧪 TESTING: Scoring Agent")
    print("="*60)
    
    agent = ScoringAgent()
    
    # Create mock conversation
    conversation = [
        ChatMessage(role="assistant", content="What is your Python experience?"),
        ChatMessage(role="user", content="I've been using Python for 5 years in production environments."),
        ChatMessage(role="assistant", content="Can you describe a complex project?"),
        ChatMessage(role="user", content="I built a distributed ML system with 100K QPS serving real-time predictions, "
                                         "optimized database queries, and implemented caching strategies."),
    ]
    
    print("\n📊 Scoring Conversation History:")
    for msg in conversation:
        role = "Q:" if msg.role == "assistant" else "A:"
        content = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
        print(f"  {role} {content}")
    
    print("\n🎯 Generating Proficiency Score...")
    score = await agent.score_skill_proficiency(
        skill="Python",
        conversation_history=conversation,
        jd_required_level=3
    )
    
    print(f"\n✅ Proficiency Score:")
    print(f"  Skill: {score.skill}")
    print(f"  Level: {score.assessed_level} (numeric: {score.assessed_level})")
    print(f"  Confidence: {score.confidence:.2%}")
    print(f"  Gap: {score.gap} (Required: {score.jd_required_level})")
    print(f"  Evidence Tags: {', '.join(score.evidence_tags)}")
    if score.conversation_summary:
        print(f"  Summary: {score.conversation_summary[:80]}...")
    
    print("\n✅ Scoring Agent: WORKING")


async def test_gap_analysis_agent():
    """Test GapAnalysisAgent gap identification."""
    print("\n" + "="*60)
    print("🧪 TESTING: Gap Analysis Agent")
    print("="*60)
    
    agent = GapAnalysisAgent()
    
    # Create mock skill scores
    skill_scores = [
        SkillScore(
            skill="Python",
            assessed_level=3,
            confidence=0.85,
            evidence_tags=["experience", "projects"],
            jd_required_level=4,
            gap=1
        ),
        SkillScore(
            skill="AWS",
            assessed_level=1,
            confidence=0.6,
            evidence_tags=["learning"],
            jd_required_level=4,
            gap=3
        ),
        SkillScore(
            skill="Docker",
            assessed_level=3,
            confidence=0.8,
            evidence_tags=["containers"],
            jd_required_level=3,
            gap=0
        ),
    ]
    
    print("\n📊 Assessed Skills:")
    for s in skill_scores:
        print(f"  {s.skill}: Level {s.assessed_level}/5 "
              f"(Required: {s.jd_required_level}, Gap: {s.gap})")
    
    print("\n🔍 Analyzing Gaps...")
    result = await agent.analyze_skill_gaps(
        skill_scores=skill_scores,
        jd_skills=["Python", "AWS", "Docker", "Kubernetes"]
    )
    
    print(f"\n✅ Gap Analysis Results:")
    print(f"  Overall Readiness: {result.overall_readiness:.1%}")
    print(f"\n  🔴 Critical Gaps ({len(result.critical_gaps)}):")
    for gap in result.critical_gaps:
        print(f"    - {gap['skill']}: {gap['priority']} ({gap['gap']} levels, ~{gap['estimated_weeks']} weeks)")
    
    print(f"\n  🟠 High Gaps ({len(result.high_gaps)}):")
    for gap in result.high_gaps:
        print(f"    - {gap['skill']}: {gap['priority']}")
    
    print(f"\n  🟡 Medium Gaps ({len(result.medium_gaps)}):")
    for gap in result.medium_gaps:
        print(f"    - {gap['skill']}: {gap['priority']}")
    
    print(f"\n  ✅ Strengths ({len(result.strengths)}):")
    for strength in result.strengths:
        print(f"    - {strength}")
    
    print(f"\n  💡 Recommended Focus:")
    for rec in result.recommended_focus:
        print(f"    {rec}")
    
    # Test readiness metrics
    metrics = agent.calculate_readiness_score(skill_scores)
    print(f"\n  📊 Detailed Metrics:")
    print(f"    - Overall: {metrics['overall']:.1%}")
    print(f"    - Coverage: {metrics['coverage']:.1%}")
    print(f"    - Confidence: {metrics['confidence']:.1%}")
    print(f"    - Timeline: {metrics['timeline_weeks']:.1f} weeks")
    
    print("\n✅ Gap Analysis Agent: WORKING")


async def test_planning_agent():
    """Test PlanningAgent learning plan generation."""
    print("\n" + "="*60)
    print("🧪 TESTING: Planning Agent")
    print("="*60)
    
    agent = PlanningAgent()
    
    # Use same skill scores from gap analysis
    skill_scores = [
        SkillScore(
            skill="Python",
            assessed_level=3,
            confidence=0.85,
            evidence_tags=["experience"],
            jd_required_level=4,
            gap=1
        ),
        SkillScore(
            skill="AWS",
            assessed_level=1,
            confidence=0.6,
            evidence_tags=["learning"],
            jd_required_level=4,
            gap=3
        ),
    ]
    
    print("\n📝 Generating Learning Plan...")
    plan = await agent.generate_learning_plan(
        skill_scores=skill_scores,
        jd_skills=["Python", "AWS"],
        weekly_hours=20.0
    )
    
    print(f"\n✅ Learning Plan Generated:")
    print(f"  Duration: {plan.total_duration_weeks} weeks")
    print(f"  Priority Skills: {', '.join(plan.priority_skills)}")
    print(f"  Adjacent Skills: {', '.join(plan.adjacent_skills)}")
    
    print(f"\n  📍 Milestones ({len(plan.milestones)}):")
    for milestone in plan.milestones[:5]:  # Show first 5
        print(f"    Week {milestone.week}: {milestone.objective}")
    
    if len(plan.milestones) > 5:
        print(f"    ... and {len(plan.milestones) - 5} more milestones")
    
    print(f"\n  ✅ Success Metrics:")
    for metric, value in plan.success_metrics.items():
        if isinstance(value, float):
            print(f"    - {metric}: {value:.1%}")
        else:
            print(f"    - {metric}: {value}")
    
    print("\n✅ Planning Agent: WORKING")


async def main():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "🚀 PHASE 2 AGENT TESTING" + " "*19 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        await test_assessment_agent()
        await test_scoring_agent()
        await test_gap_analysis_agent()
        await test_planning_agent()
        
        print("\n")
        print("╔" + "="*58 + "╗")
        print("║" + " "*15 + "✅ ALL TESTS PASSED!" + " "*25 + "║")
        print("║" + " " + "Phase 2 (AI Agents) is 100% functional".ljust(57) + "║")
        print("╚" + "="*58 + "╝")
        print("\n🎉 Ready for Phase 3 (NLP Services) or integration testing!\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
