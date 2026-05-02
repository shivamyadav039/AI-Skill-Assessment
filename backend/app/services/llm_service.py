"""
LLM Service - Wrapper around NVIDIA NIM API (OpenAI-compatible endpoint).

Features:
- NVIDIA NIM API integration via openai SDK
- Retry logic with exponential backoff
- Request/response caching (in-memory)
- Token tracking
- Fallback responses on failure
"""

import os
import time
from typing import Optional, Dict, Tuple
from loguru import logger

try:
    from openai import OpenAI
    OPENAI_SDK_AVAILABLE = True
except ImportError:
    logger.warning("openai library not available - run: pip install openai")
    OPENAI_SDK_AVAILABLE = False


# Response cache: (model, system_prompt, user_prompt) -> (response, timestamp)
_response_cache: Dict[Tuple[str, str, str], Tuple[str, float]] = {}
CACHE_EXPIRY_SECONDS = 3600  # 1 hour

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1"


class LLMService:
    """Service for interacting with NVIDIA NIM API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
    ):
        """
        Initialize the LLM Service.

        Args:
            api_key: NVIDIA API key (defaults to NVIDIA_API_KEY env var)
            model: NVIDIA NIM model to use
        """
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        self.model = model
        self.client: Optional[OpenAI] = None

        if OPENAI_SDK_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(
                    base_url=NVIDIA_BASE_URL,
                    api_key=self.api_key,
                )
                logger.info(f"✅ LLM Service initialized with NVIDIA model: {model}")
            except Exception as e:
                logger.error(f"Failed to initialize NVIDIA client: {e}")
                self.client = None
        else:
            if not self.api_key:
                logger.warning("⚠️ NVIDIA_API_KEY not set - using fallback responses")
            else:
                logger.warning("⚠️ openai SDK not available - using fallback responses")

        # Token tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        use_cache: bool = True,
        retry_count: int = 3,
    ) -> str:
        """
        Call NVIDIA NIM API with system and user prompts.

        Args:
            system_prompt: System instruction
            user_prompt: User's question/request
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)
            use_cache: Whether to use cached responses
            retry_count: Number of retries on failure

        Returns:
            Model's response text
        """
        # Check cache first
        if use_cache:
            cached = self._get_cached_response(system_prompt, user_prompt)
            if cached:
                logger.debug("Cache hit for LLM call")
                return cached

        for attempt in range(retry_count):
            try:
                response = self._call_api(system_prompt, user_prompt, max_tokens, temperature)

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
                    raise RuntimeError(f"NVIDIA LLM API unavailable after {retry_count} attempts")

        raise RuntimeError("LLM API call failed unexpectedly")

    # Keep backward-compatible alias
    def call_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        use_cache: bool = True,
        retry_count: int = 3,
    ) -> str:
        """Alias for call_llm (backward compatibility)."""
        return self.call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            use_cache=use_cache,
            retry_count=retry_count,
        )

    def _call_api(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Make actual API call to NVIDIA NIM."""
        if not self.client:
            raise RuntimeError("NVIDIA client not initialized. Set NVIDIA_API_KEY in .env")

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        response_text = completion.choices[0].message.content

        # Track usage if available
        if completion.usage:
            self.total_input_tokens += completion.usage.prompt_tokens or 0
            self.total_output_tokens += completion.usage.completion_tokens or 0
            logger.debug(
                f"NVIDIA API call succeeded - "
                f"Input: {completion.usage.prompt_tokens}, "
                f"Output: {completion.usage.completion_tokens}"
            )

        return response_text

    # ------------------------------------------------------------------ cache

    def _get_cached_response(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        cache_key = (self.model, system_prompt, user_prompt)
        if cache_key in _response_cache:
            response, timestamp = _response_cache[cache_key]
            if time.time() - timestamp < CACHE_EXPIRY_SECONDS:
                return response
            del _response_cache[cache_key]
        return None

    def _cache_response(self, system_prompt: str, user_prompt: str, response: str) -> None:
        cache_key = (self.model, system_prompt, user_prompt)
        _response_cache[cache_key] = (response, time.time())
        if len(_response_cache) > 100:
            oldest_key = min(_response_cache, key=lambda k: _response_cache[k][1])
            del _response_cache[oldest_key]

    # --------------------------------------------------------------- utilities

    def estimate_cost(self) -> Dict[str, float]:
        """Rough cost estimate (NVIDIA pricing varies by model)."""
        # Approximate: $0.001 / 1K input tokens, $0.003 / 1K output tokens
        input_cost = (self.total_input_tokens / 1000) * 0.001
        output_cost = (self.total_output_tokens / 1000) * 0.003
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "input_cost_usd": input_cost,
            "output_cost_usd": output_cost,
            "total_cost_usd": input_cost + output_cost,
        }

    def clear_cache(self) -> None:
        """Clear the response cache."""
        global _response_cache
        _response_cache.clear()
        logger.info("Response cache cleared")

    def get_cache_stats(self) -> Dict[str, int]:
        return {
            "cached_responses": len(_response_cache),
            "cache_expiry_seconds": CACHE_EXPIRY_SECONDS,
        }


# ---------------------------------------------------------------------------
# Module-level singleton + convenience function
# ---------------------------------------------------------------------------

_llm_service: Optional[LLMService] = None


def call_claude(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 500,
    temperature: float = 0.7,
    use_cache: bool = True,
    retry_count: int = 3,
) -> str:
    """
    Call NVIDIA NIM using the default LLM service instance.

    Drop-in replacement for the old call_claude() function - same signature,
    now powered by NVIDIA NIM instead of Anthropic.

    Args:
        system_prompt: System instruction
        user_prompt: User's question
        max_tokens: Maximum response tokens
        temperature: Creativity level (0-1)
        use_cache: Whether to use caching
        retry_count: Number of retries on failure

    Returns:
        Model's response text
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()

    return _llm_service.call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        use_cache=use_cache,
        retry_count=retry_count,
    )
