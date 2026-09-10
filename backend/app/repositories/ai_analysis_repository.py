from sqlalchemy.orm import Session
from app.models.ai_analysis import AiAnalysis
from app.ai.schemas import AIAnalysisResult


def create_analysis(db: Session, incident_id: int, result: AIAnalysisResult) -> AiAnalysis:
    analysis = AiAnalysis(
        incident_id=incident_id,
        severity=result.severity,
        probable_cause=result.probable_cause,
        evidence=result.evidence,
        recommendation=result.recommendation,
        summary=result.summary,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_latest_analysis(db: Session, incident_id: int) -> AiAnalysis | None:
    return (
        db.query(AiAnalysis)
        .filter(AiAnalysis.incident_id == incident_id)
        .order_by(AiAnalysis.created_at.desc())
        .first()
    )