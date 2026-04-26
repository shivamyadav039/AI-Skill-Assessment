# Agents package initialization

"""
AI Agents Module - Core intelligence for skill assessment and learning planning.

This module contains four complementary agents:
1. AssessmentAgent - Generates adaptive assessment questions
2. ScoringAgent - Evaluates proficiency from conversations
3. GapAnalysisAgent - Identifies and ranks skill gaps
4. PlanningAgent - Creates personalized learning plans
"""

from .assessment_agent import AssessmentAgent, generate_assessment_question
from .scoring_agent import ScoringAgent, score_skill_proficiency
from .gap_analysis_agent import GapAnalysisAgent, analyze_skill_gaps, GapAnalysisResult
from .planning_agent import PlanningAgent, generate_learning_plan

__all__ = [
    # Classes
    'AssessmentAgent',
    'ScoringAgent',
    'GapAnalysisAgent',
    'PlanningAgent',
    'GapAnalysisResult',
    
    # Functions
    'generate_assessment_question',
    'score_skill_proficiency',
    'analyze_skill_gaps',
    'generate_learning_plan',
]