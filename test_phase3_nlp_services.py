"""
Phase 3: NLP Services Test Suite

Test the three new NLP services:
1. SkillExtractor - Extract skills from text
2. LLMService - Call Claude API with caching
3. ResponseEvaluator - Evaluate response quality

Run with: python -m pytest test_phase3_nlp_services.py -v
Or directly: python test_phase3_nlp_services.py
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

import pytest
from loguru import logger

logger.add("test_phase3.log", rotation="1 MB")


class TestSkillExtractor:
    """Test the Skill Extractor service."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        from app.services import SkillExtractor
        self.extractor = SkillExtractor()
        yield
    
    def test_skill_extraction_basic(self):
        """Test basic skill extraction."""
        text = "We are looking for a Python expert with Django and PostgreSQL"
        skills = self.extractor.extract_skills(text)
        
        assert "Python" in skills
        assert "Django" in skills
        assert "PostgreSQL" in skills
        logger.info(f"✅ Basic extraction: {skills}")
    
    def test_skill_extraction_multiple_frameworks(self):
        """Test extraction of multiple frameworks."""
        text = "Required: React, Vue, Angular, and TypeScript experience"
        skills = self.extractor.extract_skills(text)
        
        assert "React" in skills
        assert "Vue" in skills
        assert "Angular" in skills
        assert "TypeScript" in skills
        logger.info(f"✅ Multiple frameworks: {skills}")
    
    def test_skill_extraction_cloud(self):
        """Test cloud platform extraction."""
        text = "Deploy to AWS with Kubernetes and Docker"
        skills = self.extractor.extract_skills(text)
        
        assert "AWS" in skills
        assert "Docker" in skills
        assert "Kubernetes" in skills
        logger.info(f"✅ Cloud skills: {skills}")
    
    def test_skill_extraction_empty(self):
        """Test extraction with empty text."""
        skills = self.extractor.extract_skills("")
        assert len(skills) == 0
        logger.info("✅ Empty text handling OK")
    
    def test_skill_categorization(self):
        """Test skill categorization."""
        category = self.extractor.get_skill_category("Python")
        assert category == "Programming Languages"
        
        category = self.extractor.get_skill_category("PostgreSQL")
        assert category == "Databases"
        
        logger.info("✅ Skill categorization OK")
    
    def test_skill_frequency_ranking(self):
        """Test skill frequency ranking."""
        text = "Python Python Python Django PostgreSQL"
        skills = ["Python", "Django", "PostgreSQL"]
        ranked = self.extractor.rank_skills_by_frequency(text, skills)
        
        # Python should be first (appears 3 times)
        assert ranked[0][0] == "Python"
        assert ranked[0][1] == 3
        
        logger.info(f"✅ Frequency ranking: {ranked}")


class TestLLMService:
    """Test the LLM Service."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        from app.services import LLMService
        self.llm = LLMService()
        yield
    
    def test_llm_initialization(self):
        """Test LLM service initialization."""
        assert self.llm is not None
        assert self.llm.model == "claude-3-5-sonnet-20241022"
        logger.info("✅ LLM Service initialized")
    
    def test_llm_fallback_response(self):
        """Test fallback response when API not available."""
        # Even without API, should get fallback
        response = self.llm._get_fallback_response("What is Python?")
        assert len(response) > 0
        assert isinstance(response, str)
        logger.info(f"✅ Fallback response: {response[:50]}...")
    
    def test_llm_cache_management(self):
        """Test cache operations."""
        # Test caching a response
        system = "You are helpful"
        user = "Hello"
        response = "Hi there!"
        
        self.llm._cache_response(system, user, response)
        
        # Retrieve from cache
        cached = self.llm._get_cached_response(system, user)
        assert cached == response
        
        logger.info("✅ Cache management OK")
    
    def test_llm_cache_stats(self):
        """Test cache statistics."""
        stats = self.llm.get_cache_stats()
        assert "cached_responses" in stats
        assert "cache_expiry_seconds" in stats
        logger.info(f"✅ Cache stats: {stats}")
    
    def test_llm_cost_estimation(self):
        """Test cost estimation."""
        # Add some fake token usage
        self.llm.total_input_tokens = 1000
        self.llm.total_output_tokens = 500
        
        costs = self.llm.estimate_cost()
        assert costs["total_cost"] > 0
        assert "input_cost" in costs
        assert "output_cost" in costs
        
        logger.info(f"✅ Cost estimation: ${costs['total_cost']:.4f}")


class TestResponseEvaluator:
    """Test the Response Evaluator service."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        from app.services import ResponseEvaluator
        self.evaluator = ResponseEvaluator()
        yield
    
    def test_response_evaluation_good(self):
        """Test evaluation of a good response."""
        response = (
            "I have 5 years of experience with Python. "
            "I've built several production systems using Django and FastAPI. "
            "For example, I implemented a data pipeline that processed 100M records daily, "
            "using Pandas and SQLAlchemy. The project improved reporting speed by 40%."
        )
        
        scores = self.evaluator.evaluate_response(
            response=response,
            question="Tell us about your Python experience",
            skill="Python"
        )
        
        assert scores["overall_quality"] > 0.7
        assert scores["proficiency_level"] >= 4
        assert "project" in scores["evidence_tags"]
        logger.info(f"✅ Good response evaluation: {scores['overall_quality']}")
    
    def test_response_evaluation_mediocre(self):
        """Test evaluation of a mediocre response."""
        response = "I've used Python a bit. I know some basics."
        
        scores = self.evaluator.evaluate_response(
            response=response,
            question="Tell us about your Python experience",
            skill="Python"
        )
        
        assert scores["overall_quality"] < 0.6
        assert scores["proficiency_level"] <= 2
        logger.info(f"✅ Mediocre response evaluation: {scores['overall_quality']}")
    
    def test_response_evaluation_poor(self):
        """Test evaluation of a poor response."""
        response = "Not really"
        
        scores = self.evaluator.evaluate_response(
            response=response,
            question="Tell us about your Python experience",
            skill="Python"
        )
        
        assert scores["overall_quality"] < 0.3
        assert scores["proficiency_level"] == 1
        logger.info(f"✅ Poor response evaluation: {scores['overall_quality']}")
    
    def test_evidence_tag_extraction(self):
        """Test extraction of evidence tags."""
        response = (
            "I led a team that built a distributed system. "
            "We improved performance by 50% and learned a lot about architecture."
        )
        
        scores = self.evaluator.evaluate_response(
            response=response,
            question="Tell us about your experience",
            skill="Architecture"
        )
        
        tags = scores["evidence_tags"]
        assert "project" in tags or "team" in tags
        assert "metrics" in tags or "learning" in tags
        logger.info(f"✅ Evidence tags: {tags}")
    
    def test_response_comparison(self):
        """Test comparing two responses."""
        response1 = "I have used Python for years and built many projects."
        response2 = "Not much experience with Python."
        
        comparison = self.evaluator.compare_responses(
            response1=response1,
            response2=response2,
            question="Tell us about Python"
        )
        
        assert comparison["better_response"] == 1
        assert comparison["response1_quality"] > comparison["response2_quality"]
        logger.info(f"✅ Response comparison: Response 1 is better")
    
    def test_proficiency_level_mapping(self):
        """Test quality score to proficiency mapping."""
        test_cases = [
            (0.1, 1),  # 0.1 -> Beginner
            (0.3, 2),  # 0.3 -> Elementary
            (0.5, 3),  # 0.5 -> Intermediate
            (0.7, 4),  # 0.7 -> Advanced
            (0.9, 5),  # 0.9 -> Expert
        ]
        
        for score, expected_level in test_cases:
            level = self.evaluator._score_to_proficiency_level(score)
            assert level == expected_level
        
        logger.info("✅ Proficiency level mapping OK")


class TestPhase3Integration:
    """Integration tests for Phase 3 services."""
    
    def test_skill_extraction_real_jd(self):
        """Test skill extraction on realistic job description."""
        from app.services import extract_skills
        
        jd = """
        Senior Backend Engineer - Python
        
        We are looking for an experienced Python developer with:
        - 5+ years of Python development
        - Experience with FastAPI or Django
        - Strong PostgreSQL and Redis knowledge
        - Kubernetes and Docker deployment experience
        - AWS or GCP cloud platform experience
        - RESTful API design and GraphQL
        
        Nice to have:
        - Machine Learning with TensorFlow or PyTorch
        - Data pipeline experience with Spark
        """
        
        skills = extract_skills(jd)
        
        assert "Python" in skills
        assert "FastAPI" in skills or "Django" in skills
        assert "PostgreSQL" in skills
        assert "Docker" in skills
        assert "Kubernetes" in skills
        
        logger.info(f"✅ Real JD extraction: {len(skills)} skills found")
    
    def test_end_to_end_workflow(self):
        """Test complete Phase 3 workflow."""
        from app.services import extract_skills, evaluate_response_quality, call_claude
        
        # Step 1: Extract skills from JD
        jd = "Looking for Python expert with Django and PostgreSQL"
        jd_skills = extract_skills(jd)
        logger.info(f"JD Skills: {jd_skills}")
        
        # Step 2: Extract skills from resume
        resume = "I have 3 years Python experience and used Django in recent projects"
        resume_skills = extract_skills(resume)
        logger.info(f"Resume Skills: {resume_skills}")
        
        # Step 3: Evaluate a response
        response = "I built several Django applications with PostgreSQL databases"
        scores = evaluate_response_quality(
            response=response,
            question="Tell us about Django experience",
            skill="Django"
        )
        logger.info(f"Response Quality: {scores['overall_quality']}")
        
        # Step 4: Test LLM service (fallback only)
        fallback_response = call_claude(
            system_prompt="You are helpful",
            user_prompt="Test"
        )
        logger.info(f"LLM Response: {fallback_response[:50]}...")
        
        assert len(jd_skills) > 0
        assert len(resume_skills) > 0
        assert scores["overall_quality"] > 0
        logger.info("✅ E2E workflow successful")


def run_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("Phase 3: NLP Services Test Suite")
    print("="*70 + "\n")
    
    # Run pytest
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-ra"
    ])
    
    print("\n" + "="*70)
    if exit_code == 0:
        print("✅ All Phase 3 tests passed!")
    else:
        print("❌ Some tests failed")
    print("="*70)
    
    return exit_code


if __name__ == "__main__":
    # Run without pytest if called directly
    print("Running Phase 3 NLP Services Tests...\n")
    
    try:
        # Test Skill Extractor
        print("🧪 Testing Skill Extractor...")
        from app.services import SkillExtractor
        extractor = SkillExtractor()
        skills = extractor.extract_skills("Python Django PostgreSQL")
        print(f"   ✅ Extracted skills: {skills}\n")
        
        # Test LLM Service
        print("🧪 Testing LLM Service...")
        from app.services import LLMService
        llm = LLMService()
        response = llm._get_fallback_response("test")
        print(f"   ✅ LLM fallback works\n")
        
        # Test Response Evaluator
        print("🧪 Testing Response Evaluator...")
        from app.services import ResponseEvaluator
        evaluator = ResponseEvaluator()
        scores = evaluator.evaluate_response(
            response="I have 5 years experience",
            question="Tell me about yourself",
            skill="Python"
        )
        print(f"   ✅ Response evaluated: quality={scores['overall_quality']}\n")
        
        print("✅ All Phase 3 services working!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
