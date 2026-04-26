"""
Skill Extractor Service - NLP-based skill extraction from JD and Resume.

Phase 3: Replace placeholder skill extraction with real NLP processing.

Features:
- Uses spaCy for NER (Named Entity Recognition)
- Sentence-transformers for semantic similarity
- Custom skill taxonomy matching
- Handles technical skills, tools, languages, frameworks
"""

import os
from typing import List, Set, Dict, Tuple
from loguru import logger

try:
    import spacy
    from sentence_transformers import SentenceTransformer, util
    SPACY_AVAILABLE = True
except ImportError:
    logger.warning("spacy or sentence-transformers not available - using fallback")
    SPACY_AVAILABLE = False


# Common technical skills taxonomy
TECH_SKILLS_TAXONOMY = {
    "Programming Languages": [
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "Go", 
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "Elixir"
    ],
    "Frameworks & Libraries": [
        "FastAPI", "Django", "Flask", "Spring", "SpringBoot", "React", "Vue", 
        "Angular", "Next.js", "Express", "TensorFlow", "PyTorch", "Scikit-learn",
        "Pandas", "NumPy", "SQLAlchemy", "Hibernate"
    ],
    "Databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", 
        "DynamoDB", "Cassandra", "Oracle", "SQL Server", "Firebase"
    ],
    "Cloud Platforms": [
        "AWS", "Azure", "GCP", "Google Cloud", "Kubernetes", "Docker", 
        "Docker Compose", "Helm", "Lambda", "EC2", "S3"
    ],
    "Development Tools": [
        "Git", "GitHub", "GitLab", "Jenkins", "CI/CD", "Docker", "Kubernetes",
        "Terraform", "Ansible", "Linux", "Unix", "Shell", "Bash"
    ],
    "Data & ML": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", 
        "Data Science", "Analytics", "Big Data", "Spark", "Hadoop", "Data Engineering"
    ],
    "Web & APIs": [
        "REST API", "GraphQL", "WebSocket", "gRPC", "HTTP", "OAuth", 
        "JWT", "Microservices", "API Design"
    ],
    "Other Technical": [
        "Agile", "Scrum", "OOP", "Design Patterns", "Testing", "Unit Testing",
        "Integration Testing", "Performance Optimization", "Security", "DevOps"
    ]
}

# Flatten taxonomy for quick lookup
FLAT_SKILLS_SET = set()
SKILLS_CONTEXT = {}  # skill -> category mapping

for category, skills in TECH_SKILLS_TAXONOMY.items():
    for skill in skills:
        FLAT_SKILLS_SET.add(skill.lower())
        SKILLS_CONTEXT[skill.lower()] = category


class SkillExtractor:
    """Extract technical skills from job descriptions and resumes."""
    
    def __init__(self):
        """Initialize the skill extractor."""
        self.nlp = None
        self.sentence_model = None
        self.similarity_threshold = 0.75
        
        # Try to load spaCy model
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("✅ spaCy model loaded")
            except OSError:
                logger.warning("⚠️ spaCy model not found - install with: python -m spacy download en_core_web_sm")
                self.nlp = None
        
        # Try to load sentence transformer
        if SPACY_AVAILABLE:
            try:
                self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("✅ Sentence transformer model loaded")
            except Exception as e:
                logger.warning(f"⚠️ Could not load sentence transformer: {e}")
                self.sentence_model = None
        
        logger.info("🤖 Skill Extractor initialized")
    
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills from text using NLP.
        
        Strategy:
        1. Keyword matching against taxonomy (fast, high-precision)
        2. Semantic similarity matching (catches variations, slower)
        3. NER-based extraction (catch domain-specific terms)
        
        Args:
            text: Text to extract skills from (JD or Resume)
            
        Returns:
            List of unique extracted skills
            
        Example:
            >>> extractor = SkillExtractor()
            >>> skills = extractor.extract_skills(
            ...     "Looking for Python expert with Django and PostgreSQL experience"
            ... )
            >>> print(skills)
            ['Python', 'Django', 'PostgreSQL']
        """
        if not text:
            return []
        
        extracted = set()
        
        # Strategy 1: Direct keyword matching
        extracted.update(self._keyword_matching(text))
        
        # Strategy 2: Semantic similarity (if available)
        if self.sentence_model:
            extracted.update(self._semantic_matching(text))
        
        # Strategy 3: NER-based extraction (if spacy available)
        if self.nlp:
            extracted.update(self._ner_extraction(text))
        
        return sorted(list(extracted))
    
    
    def _keyword_matching(self, text: str) -> Set[str]:
        """
        Fast keyword matching against the skills taxonomy.
        
        Args:
            text: Text to search
            
        Returns:
            Set of found skills
        """
        found_skills = set()
        text_lower = text.lower()
        
        # Check each skill in taxonomy
        for skill in FLAT_SKILLS_SET:
            # Whole-word matching to avoid false positives
            # e.g., "Python" should match but not "Pythonic"
            if f" {skill} " in f" {text_lower} ":
                # Find original casing from taxonomy
                for category, skills in TECH_SKILLS_TAXONOMY.items():
                    for s in skills:
                        if s.lower() == skill:
                            found_skills.add(s)
                            break
        
        return found_skills
    
    
    def _semantic_matching(self, text: str) -> Set[str]:
        """
        Find skills using semantic similarity.
        
        Catches variations like "Python programming" -> Python
        
        Args:
            text: Text to search
            
        Returns:
            Set of found skills through semantic similarity
        """
        found_skills = set()
        
        if not self.sentence_model:
            return found_skills
        
        try:
            # Split text into sentences and phrases
            sentences = text.split(".")
            phrases = []
            for sent in sentences:
                # Extract noun phrases (simplified)
                parts = sent.split(",")
                phrases.extend([p.strip() for p in parts if len(p.strip()) > 3])
            
            if not phrases:
                return found_skills
            
            # Encode phrases
            phrase_embeddings = self.sentence_model.encode(phrases, convert_to_tensor=True)
            
            # Check each skill from taxonomy
            for category, skills in TECH_SKILLS_TAXONOMY.items():
                skill_embeddings = self.sentence_model.encode(skills, convert_to_tensor=True)
                
                # Calculate similarity
                similarities = util.pytorch_cos_sim(phrase_embeddings, skill_embeddings)
                
                # Find matches above threshold
                for i, phrase in enumerate(phrases):
                    for j, skill in enumerate(skills):
                        similarity = similarities[i][j].item()
                        if similarity > self.similarity_threshold and skill.lower() not in phrase.lower():
                            # Avoid duplicates from keyword matching
                            found_skills.add(skill)
                            logger.debug(f"Semantic match: '{phrase}' -> '{skill}' ({similarity:.2f})")
        
        except Exception as e:
            logger.warning(f"Error in semantic matching: {e}")
        
        return found_skills
    
    
    def _ner_extraction(self, text: str) -> Set[str]:
        """
        Extract skills using spaCy NER.
        
        Args:
            text: Text to process
            
        Returns:
            Set of found skills
        """
        found_skills = set()
        
        if not self.nlp:
            return found_skills
        
        try:
            doc = self.nlp(text)
            
            # Look for relevant entities and patterns
            for ent in doc.ents:
                # ORG entities sometimes contain tool/framework names
                if ent.label_ == "ORG":
                    ent_lower = ent.text.lower()
                    for skill in FLAT_SKILLS_SET:
                        if skill in ent_lower:
                            # Find original casing
                            for s_cat, s_list in TECH_SKILLS_TAXONOMY.items():
                                for s in s_list:
                                    if s.lower() == skill:
                                        found_skills.add(s)
                                        break
        
        except Exception as e:
            logger.warning(f"Error in NER extraction: {e}")
        
        return found_skills
    
    
    def get_skill_category(self, skill: str) -> str:
        """
        Get the category of a skill.
        
        Args:
            skill: Skill name
            
        Returns:
            Category name or "Other"
        """
        return SKILLS_CONTEXT.get(skill.lower(), "Other")
    
    
    def rank_skills_by_frequency(self, text: str, skills: List[str]) -> List[Tuple[str, int]]:
        """
        Rank skills by frequency in text.
        
        Args:
            text: Source text
            skills: List of skills to rank
            
        Returns:
            List of (skill, frequency) tuples, sorted by frequency
        """
        text_lower = text.lower()
        ranked = []
        
        for skill in skills:
            # Count occurrences (case-insensitive)
            count = text_lower.count(skill.lower())
            if count > 0:
                ranked.append((skill, count))
        
        # Sort by frequency (descending)
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked


# Module-level convenience function

_extractor = None

def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text using the default extractor.
    
    Convenience function for use in endpoints.
    
    Args:
        text: Text to extract skills from
        
    Returns:
        List of extracted skills
    """
    global _extractor
    if _extractor is None:
        _extractor = SkillExtractor()
    
    return _extractor.extract_skills(text)
