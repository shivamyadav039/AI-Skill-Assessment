"""
Quick Reference: API Data Contracts

This file documents all request/response schemas for the backend API.
Use this as a reference for frontend development and API testing.
"""

# ============ 1. UPLOAD DOCUMENTS ============
# Endpoint: POST /api/v1/upload
# Purpose: Upload JD and Resume, extract skills, create session

REQUEST_UPLOAD = {
    "jd_content": "str (required) - Job description text",
    "resume_content": "str (required) - Resume text",
    "candidate_name": "str (optional) - Candidate name"
}

RESPONSE_UPLOAD = {
    "session_id": "str - Unique session ID (use in all subsequent requests)",
    "jd_skills": "List[str] - Skills extracted from JD",
    "resume_skills": "List[str] - Skills extracted from resume",
    "total_skills_to_assess": "int - Number of skills to assess",
    "timestamp": "datetime - When upload occurred"
}

EXAMPLE_UPLOAD_REQUEST = {
    "jd_content": "We are looking for a Senior Python Engineer with experience in system design, AWS, and PostgreSQL. Must have 5+ years of production experience and strong problem-solving skills.",
    "resume_content": "John Doe\n5 years Software Engineer at TechCorp\nSkills: Python, JavaScript, AWS, Docker, Git\nEducation: BS Computer Science",
    "candidate_name": "John Doe"
}

EXAMPLE_UPLOAD_RESPONSE = {
    "session_id": "session_a1b2c3d4e5f6",
    "jd_skills": ["Python", "System Design", "AWS", "PostgreSQL", "Problem Solving"],
    "resume_skills": ["Python", "JavaScript", "AWS", "Docker", "Git"],
    "total_skills_to_assess": 5,
    "timestamp": "2024-04-25T10:30:00Z"
}


# ============ 2. CHAT / CONVERSATIONAL ASSESSMENT ============
# Endpoint: POST /api/v1/chat
# Purpose: Run adaptive multi-turn conversation per skill

REQUEST_CHAT = {
    "session_id": "str (required) - From upload response",
    "skill": "str (required) - Skill being assessed",
    "user_message": "str (required) - User's response to question",
    "turn_count": "int (optional, default=1) - Conversation turn number"
}

RESPONSE_CHAT = {
    "session_id": "str - Session ID",
    "skill": "str - Current skill",
    "assistant_message": "str - Next assessment question or feedback",
    "turn_count": "int - Next turn number",
    "conversation_history": "List[ChatMessage] - Full conversation so far",
    "assessment_complete": "bool - Is this skill assessment done?",
    "next_skill": "str or null - Next skill to assess, or null if all done"
}

EXAMPLE_CHAT_REQUEST = {
    "session_id": "session_a1b2c3d4e5f6",
    "skill": "Python",
    "user_message": "I have used Python for 5 years in production at TechCorp. I've built REST APIs, data pipelines, and worked with Django and FastAPI. I'm comfortable with async programming and have experience with unit testing.",
    "turn_count": 1
}

EXAMPLE_CHAT_RESPONSE = {
    "session_id": "session_a1b2c3d4e5f6",
    "skill": "Python",
    "assistant_message": "Excellent! You have solid production experience. Let me ask you a scenario-based question: Imagine you're building a high-throughput API that needs to handle 10,000 requests per second with heavy database operations. How would you design the Python backend to optimize for performance? What patterns and libraries would you use?",
    "turn_count": 2,
    "conversation_history": [
        {
            "role": "assistant",
            "content": "Tell me about your experience with Python. What projects have you worked on and what concepts are you most comfortable with?",
            "timestamp": "2024-04-25T10:30:00Z"
        },
        {
            "role": "user",
            "content": "I have used Python for 5 years in production at TechCorp...",
            "timestamp": "2024-04-25T10:30:30Z"
        },
        {
            "role": "assistant",
            "content": "Excellent! You have solid production experience...",
            "timestamp": "2024-04-25T10:31:00Z"
        }
    ],
    "assessment_complete": False,
    "next_skill": None
}


# ============ 3. SKILL SCORING ============
# Endpoint: POST /api/v1/score
# Purpose: Score proficiency for a completed skill assessment

REQUEST_SCORE = {
    "session_id": "str (required) - Session ID",
    "skill": "str (required) - Skill to score"
}

RESPONSE_SCORE = {
    "session_id": "str - Session ID",
    "skill_score": {
        "skill": "str - Skill name",
        "assessed_level": "int (1-5) - Proficiency level from assessment",
        "confidence": "float (0-1) - Confidence of assessment",
        "jd_required_level": "int (1-5) - Level required by JD",
        "gap": "int - jd_required_level - assessed_level",
        "evidence_tags": "List[str] - Tags supporting the score",
        "conversation_summary": "str - Summary of assessment conversation"
    },
    "all_scores": "List[SkillScore] or null - All scores if all skills assessed"
}

EXAMPLE_SCORE_REQUEST = {
    "session_id": "session_a1b2c3d4e5f6",
    "skill": "Python"
}

EXAMPLE_SCORE_RESPONSE = {
    "session_id": "session_a1b2c3d4e5f6",
    "skill_score": {
        "skill": "Python",
        "assessed_level": 4,
        "confidence": 0.92,
        "jd_required_level": 4,
        "gap": 0,
        "evidence_tags": [
            "strong_fundamentals",
            "production_experience",
            "async_programming",
            "api_design",
            "testing_knowledge"
        ],
        "conversation_summary": "Candidate demonstrates excellent Python proficiency with 5 years production experience. Strong understanding of async patterns, API design, and best practices. Confidently answered advanced scenario-based questions. Slight uncertainty on metaclass usage, but overall expert-level knowledge."
    },
    "all_scores": None
}


# ============ 4. LEARNING PLAN GENERATION ============
# Endpoint: POST /api/v1/plan
# Purpose: Generate personalized learning roadmap

REQUEST_PLAN = {
    "session_id": "str (required) - Session ID"
}

RESPONSE_PLAN = {
    "learning_plan": {
        "session_id": "str - Session ID",
        "candidate_name": "str or null - Candidate name",
        "total_duration_weeks": "int - Total weeks for plan",
        "priority_skills": "List[str] - High-gap skills to focus on",
        "adjacent_skills": "List[str] - Skills that build on existing knowledge",
        "milestones": [
            {
                "week": "int - Week number",
                "skill": "str - Skill for this milestone",
                "objective": "str - Learning objective",
                "resources": [
                    {
                        "title": "str - Resource title",
                        "description": "str - Resource description",
                        "url": "str or null - URL to resource",
                        "resource_type": "str - 'course', 'book', 'tutorial', 'practice'",
                        "estimated_duration_hours": "int - Time to complete",
                        "difficulty_level": "str - 'beginner', 'intermediate', 'advanced'",
                        "relevance_score": "float (0-1) - How relevant to skill"
                    }
                ],
                "prerequisite_skills": "List[str] - Skills needed before this",
                "assessment_criteria": "List[str] - How to assess completion"
            }
        ],
        "success_metrics": {
            "target_proficiency": "float - Target skill level",
            "timeline_adherence": "str - Expected timeline adherence %",
            "resource_completion": "str - Expected completion rate",
            "assessment_score": "str - Expected assessment score"
        },
        "created_at": "datetime - When plan was created"
    },
    "summary": "str - Executive summary of the plan"
}

EXAMPLE_PLAN_RESPONSE = {
    "learning_plan": {
        "session_id": "session_a1b2c3d4e5f6",
        "candidate_name": "John Doe",
        "total_duration_weeks": 8,
        "priority_skills": ["System Design", "PostgreSQL Advanced"],
        "adjacent_skills": ["Database Optimization", "Cache Patterns", "API Scaling"],
        "milestones": [
            {
                "week": 1,
                "skill": "System Design Fundamentals",
                "objective": "Understand scalability, databases, caching patterns, and distributed systems",
                "resources": [
                    {
                        "title": "System Design Interview Course",
                        "description": "Comprehensive guide to designing scalable systems",
                        "url": "https://example.com/system-design",
                        "resource_type": "course",
                        "estimated_duration_hours": 30,
                        "difficulty_level": "advanced",
                        "relevance_score": 0.95
                    },
                    {
                        "title": "Designing Data-Intensive Applications",
                        "description": "Deep dive into system design principles",
                        "url": None,
                        "resource_type": "book",
                        "estimated_duration_hours": 40,
                        "difficulty_level": "advanced",
                        "relevance_score": 0.90
                    }
                ],
                "prerequisite_skills": ["Database Fundamentals", "API Design"],
                "assessment_criteria": [
                    "Design a Twitter-like system",
                    "Design Netflix streaming",
                    "Quiz on CAP theorem"
                ]
            },
            {
                "week": 2,
                "skill": "PostgreSQL Advanced Patterns",
                "objective": "Master indexing, query optimization, and replication",
                "resources": [
                    {
                        "title": "PostgreSQL Query Optimization",
                        "description": "Advanced PostgreSQL performance tuning",
                        "url": "https://example.com/postgres-opt",
                        "resource_type": "course",
                        "estimated_duration_hours": 20,
                        "difficulty_level": "advanced",
                        "relevance_score": 0.92
                    }
                ],
                "prerequisite_skills": ["SQL Fundamentals", "Database Design"],
                "assessment_criteria": [
                    "Optimize 5 complex queries",
                    "Design indexing strategy",
                    "Hands-on replication setup"
                ]
            }
        ],
        "success_metrics": {
            "target_proficiency": 4.5,
            "timeline_adherence": "95%",
            "resource_completion": "100%",
            "assessment_score": ">= 85%"
        },
        "created_at": "2024-04-25T10:35:00Z"
    },
    "summary": "Your personalized 8-week learning plan is ready! Focus on System Design and PostgreSQL optimization to close skill gaps. Plan emphasizes hands-on practice with adjacent skills that build on your Python expertise. Estimated time commitment: 4-5 hours/week."
}


# ============ 5. GAP ANALYSIS ============
# Endpoint: GET /api/v1/gaps/{session_id}
# Purpose: Retrieve gap analysis for completed assessments

RESPONSE_GAP_ANALYSIS = {
    "session_id": "str - Session ID",
    "gaps": [
        {
            "skill": "str - Skill name",
            "assessed_level": "int (1-5) - Level from assessment",
            "jd_required_level": "int (1-5) - Required by JD",
            "gap_severity": "str - 'critical', 'high', 'medium', 'low'",
            "priority_rank": "int - Priority order (1 = highest)",
            "upskilling_path": "List[str] - Adjacent skills to learn first"
        }
    ],
    "overall_readiness": "float (0-1) - Overall JD readiness percentage"
}

EXAMPLE_GAP_RESPONSE = {
    "session_id": "session_a1b2c3d4e5f6",
    "gaps": [
        {
            "skill": "System Design",
            "assessed_level": 2,
            "jd_required_level": 4,
            "gap_severity": "critical",
            "priority_rank": 1,
            "upskilling_path": ["Database Design", "API Scaling", "Distributed Systems", "System Design"]
        },
        {
            "skill": "PostgreSQL",
            "assessed_level": 3,
            "jd_required_level": 4,
            "gap_severity": "high",
            "priority_rank": 2,
            "upskilling_path": ["Query Optimization", "Indexing Strategies", "PostgreSQL Advanced"]
        },
        {
            "skill": "Python",
            "assessed_level": 4,
            "jd_required_level": 4,
            "gap_severity": "low",
            "priority_rank": 3,
            "upskilling_path": []
        },
        {
            "skill": "AWS",
            "assessed_level": 3,
            "jd_required_level": 4,
            "gap_severity": "medium",
            "priority_rank": 4,
            "upskilling_path": ["RDS Advanced", "ElastiCache", "AWS Solutions Architect"]
        }
    ],
    "overall_readiness": 0.65
}


# ============ PROFICIENCY LEVELS ============
# Used in assessed_level, jd_required_level, target_proficiency

PROFICIENCY_LEVELS = {
    1: "Beginner - Basic understanding, minimal practical experience",
    2: "Elementary - Some hands-on experience, limited production use",
    3: "Intermediate - Good working knowledge, comfortable with common tasks",
    4: "Advanced - Expert knowledge, can handle complex scenarios and optimization",
    5: "Expert - Mastery level, can architect solutions and mentor others"
}


# ============ EVIDENCE TAGS ============
# Tags that back up proficiency scores extracted from conversations

EVIDENCE_TAGS = [
    "strong_fundamentals",          # Understands core concepts
    "production_experience",         # Used in real systems
    "api_design",                    # Can design APIs
    "async_programming",             # Knows async patterns
    "testing_knowledge",             # Understands testing
    "optimization_experience",       # Has optimized systems
    "system_architecture",           # Can design systems
    "demonstrates_concepts",         # Can explain concepts clearly
    "partial_implementation",        # Has implemented but incomplete
    "limited_scenarios",             # Limited real-world experience
    "theoretical_only",              # Only book knowledge
    "hands_on_practice",             # Practical skills
    "problem_solving",               # Good at debugging
    "collaboration_experience",      # Team experience
]


# ============ TESTING QUICK CURL COMMANDS ============

"""
# Test Upload
curl -X POST http://localhost:8000/api/v1/upload \
  -H "Content-Type: application/json" \
  -d '{
    "jd_content": "Senior Python Engineer required...",
    "resume_content": "John Doe, 5 years Python...",
    "candidate_name": "John Doe"
  }'

# Test Chat (use session_id from upload)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_xxx",
    "skill": "Python",
    "user_message": "I have 5 years Python experience...",
    "turn_count": 1
  }'

# Test Score
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_xxx",
    "skill": "Python"
  }'

# Test Plan
curl -X POST http://localhost:8000/api/v1/plan \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_xxx"
  }'

# Test Gap Analysis
curl http://localhost:8000/api/v1/gaps/session_xxx

# Health Check
curl http://localhost:8000/health
"""
