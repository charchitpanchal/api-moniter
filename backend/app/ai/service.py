import json
import logging
from pydantic import ValidationError
from app.ai.schemas import IncidentContext, AIAnalysisResult, SummaryResult
from app.ai.prompts import SYSTEM_PROMPT, build_incident_analysis_prompt, SUMMARY_SYSTEM_PROMPT, build_summary_prompt
from app.ai.provider import get_provider
from app.core.config import settings

logger = logging.getLogger("ai.service")


def _extract_json(raw_text: str) -> dict:
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


async def analyze_incident(context: IncidentContext) -> AIAnalysisResult | None:
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


async def summarize_incident(context: IncidentContext) -> SummaryResult | None:
    """
    Generates a short, plain-English summary — separate from the full
    root-cause analysis, intended for non-technical status updates.
    Not persisted to DB (cheap to regenerate on demand).
    """
    if not settings.ai_enabled:
        logger.info("AI summary skipped: AI_ENABLED is false.")
        return None

    try:
        provider = get_provider()
        user_prompt = build_summary_prompt(context)

        raw_response = await provider.generate(SUMMARY_SYSTEM_PROMPT, user_prompt)
        parsed = _extract_json(raw_response)

        result = SummaryResult(**parsed)
        logger.info("AI summary succeeded.")
        return result

    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"AI summary response failed validation: {e}")
        return None
    except Exception as e:
        logger.error(f"AI summary provider call failed: {e}")
        return None