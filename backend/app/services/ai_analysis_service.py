import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.incident import Incident
from app.ai.context_builder import build_incident_context
from app.ai.service import analyze_incident
from app.repositories import ai_analysis_repository

logger = logging.getLogger("services.ai_analysis")


async def run_analysis_for_incident(db: Session, incident: Incident):
    """
    Orchestrates: build context -> call AI -> store result.
    Raises a clean 503 if AI is unavailable/disabled/failed — the incident
    itself is never modified or harmed by an AI failure.
    """
    context = build_incident_context(db, incident)
    result = await analyze_incident(context)

    if result is None:
        logger.warning(f"AI analysis unavailable for incident #{incident.id}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI analysis is currently unavailable. The incident is unaffected; please try again later.",
        )

    analysis = ai_analysis_repository.create_analysis(db, incident.id, result)
    logger.info(f"AI analysis stored for incident #{incident.id} (analysis #{analysis.id})")
    return analysis


def get_latest_analysis_or_404(db: Session, incident_id: int):
    analysis = ai_analysis_repository.get_latest_analysis(db, incident_id)
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No AI analysis exists yet for this incident.",
        )
    return analysis