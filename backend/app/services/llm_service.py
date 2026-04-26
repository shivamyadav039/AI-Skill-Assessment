"""
LLM Service - Wrapper around Google Gemini API with caching and error handling.

Features:
- Google Gemini API integration (gemini-1.5-flash by default)
- Retry logic with exponential backoff
- Request/response caching (in-memory)
- Fallback responses on failure
"""

import os
import time
import json
from typing import Optional, Dict, List, Tuple
from loguru import logger
from functools import lru_cache

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    logger.warning("google-generativeai library not available - using fallback responses")
    GEMINI_AVAILABLE = False


# Response cache: (model, system_prompt, user_prompt) -> (response, timestamp)
_response_cache: Dict[Tuple[str, str, str], Tuple[str, float]] = {}
CACHE_EXPIRY_SECONDS = 3600  # 1 hour


class LLMService:
    """Service for interacting with Google Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        """
        Initialize the LLM Service.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Gemini model to use
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.client = None

        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.client = True  # marker — genai uses module-level config
                logger.info(f"✅ LLM Service initialized with {model}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            logger.warning("⚠️ Gemini client not available - using fallback responses")

        # Tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    
    def call_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        use_cache: bool = True,
        retry_count: int = 3
    ) -> str:
        """
        Call Gemini API with system and user prompts.
        (Method name kept as call_claude for backward compatibility.)

        Args:
            system_prompt: System instruction for Gemini
            user_prompt: User's question/request
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)
            use_cache: Whether to use cached responses
            retry_count: Number of retries on failure

        Returns:
            Gemini's response text
        """
        # Check cache first
        if use_cache:
            cached_response = self._get_cached_response(system_prompt, user_prompt)
            if cached_response:
                logger.debug("Cache hit for Gemini call")
                return cached_response

        # Try API call with retries
        for attempt in range(retry_count):
            try:
                response = self._call_gemini_api(
                    system_prompt, user_prompt, max_tokens, temperature
                )

                # Cache successful response
                if use_cache:
                    self._cache_response(system_prompt, user_prompt, response)

                return response

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{retry_count} failed: {e}")

                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {retry_count} attempts failed")
                    return self._get_fallback_response(user_prompt)

        return self._get_fallback_response(user_prompt)
    
    
    def _call_gemini_api(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """
        Make actual API call to Gemini.

        Args:
            system_prompt: System instruction
            user_prompt: User message
            max_tokens: Max response tokens
            temperature: Creativity level

        Returns:
            Response text from Gemini

        Raises:
            Exception on API errors
        """
        if not self.client:
            raise RuntimeError("Gemini client not initialized")

        try:
            model = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=system_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            response = model.generate_content(user_prompt)
            response_text = response.text

            logger.debug("Gemini API call succeeded")
            return response_text

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    
    def _get_cached_response(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Get response from cache if available and not expired.
        
        Args:
            system_prompt: System instruction
            user_prompt: User message
            
        Returns:
            Cached response or None
        """
        cache_key = (self.model, system_prompt, user_prompt)
        
        if cache_key in _response_cache:
            response, timestamp = _response_cache[cache_key]
            
            # Check if expired
            if time.time() - timestamp < CACHE_EXPIRY_SECONDS:
                return response
            else:
                # Remove expired entry
                del _response_cache[cache_key]
        
        return None
    
    
    def _cache_response(self, system_prompt: str, user_prompt: str, response: str) -> None:
        """
        Cache a response.
        
        Args:
            system_prompt: System instruction
            user_prompt: User message
            response: Response to cache
        """
        cache_key = (self.model, system_prompt, user_prompt)
        _response_cache[cache_key] = (response, time.time())
        
        # Simple cache size management (keep last 100 entries)
        if len(_response_cache) > 100:
            # Remove oldest entry
            oldest_key = min(_response_cache.keys(), key=lambda k: _response_cache[k][1])
            del _response_cache[oldest_key]
    
    
    def _get_fallback_response(self, user_prompt: str) -> str:
        """
        Get fallback response when API fails.
        
        Args:
            user_prompt: Original user prompt
            
        Returns:
            Template-based fallback response
        """
        logger.warning("Using fallback response")
        
        # Detect prompt type and provide appropriate fallback
        if "question" in user_prompt.lower():
            return "Can you provide more details about your experience with this topic? Please share a specific example from your past projects."
        elif "score" in user_prompt.lower() or "proficiency" in user_prompt.lower():
            return "Based on your responses, your proficiency level appears to be intermediate with room for growth in advanced concepts."
        elif "plan" in user_prompt.lower() or "learn" in user_prompt.lower():
            return "A good learning path would be: 1) Master the fundamentals through practice, 2) Work on real-world projects, 3) Study advanced patterns and best practices."
        else:
            return "Thank you for your input. This is helpful for understanding your background and experience level."
    
    
    def estimate_cost(self) -> Dict[str, float]:
        """Placeholder cost estimate (Gemini pricing varies by tier)."""
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "note": "Gemini free-tier has no per-token cost; see cloud.google.com for paid pricing."
        }
    
    
    def clear_cache(self) -> None:
        """Clear the response cache."""
        global _response_cache
        _response_cache.clear()
        logger.info("Response cache cleared")
    
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Dict with cache info
        """
        return {
            "cached_responses": len(_response_cache),
            "cache_expiry_seconds": CACHE_EXPIRY_SECONDS
        }


# Module-level convenience function

_llm_service = None

def call_claude(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 500,
    temperature: float = 0.7,
    use_cache: bool = True
) -> str:
    """
    Call Claude using the default LLM service instance.
    
    Convenience function for use in agents and endpoints.
    
    Args:
        system_prompt: System instruction for Claude
        user_prompt: User's question
        max_tokens: Maximum response tokens
        temperature: Creativity level (0-1)
        use_cache: Whether to use caching
        
    Returns:
        Claude's response text
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    
    return _llm_service.call_claude(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        use_cache=use_cache
    )
