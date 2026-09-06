import json
import logging
from pydantic import ValidationError
from app.ai.schemas import IncidentContext, AIAnalysisResult
from app.ai.prompts import SYSTEM_PROMPT, build_incident_analysis_prompt
from app.ai.provider import get_provider
from app.core.config import settings

logger = logging.getLogger("ai.service")


def _extract_json(raw_text: str) -> dict:
    """
    LLMs sometimes wrap JSON in markdown code fences despite instructions.
    Strip that defensively before parsing.
    """
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


async def analyze_incident(context: IncidentContext) -> AIAnalysisResult | None:
    """
    The ONLY function the rest of the app should call for AI incident analysis.
    Returns None on ANY failure (disabled, provider error, invalid response) —
    callers must handle None gracefully. AI failures NEVER raise exceptions
    that could interrupt monitoring or incident management.
    """
    if not settings.ai_enabled:
        logger.info("AI analysis skipped: AI_ENABLED is false.")
        return None

    try:
        provider = get_provider()
        user_prompt = build_incident_analysis_prompt(context)

        raw_response = await provider.generate(SYSTEM_PROMPT, user_prompt)
        parsed = _extract_json(raw_response)

        result = AIAnalysisResult(**parsed)
        logger.info(f"AI analysis succeeded: severity={result.severity}")
        return result

    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"AI response failed validation: {e}")
        return None
    except Exception as e:
        logger.error(f"AI provider call failed: {e}")
        return None