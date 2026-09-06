import logging
from sqlalchemy.orm import Session
from app.models.incident import Incident, IncidentSeverity
from app.notifications.provider import get_notification_provider

logger = logging.getLogger("notifications.service")


async def notify_if_needed(db: Session, incident: Incident) -> None:
    """
    Sends exactly one alert per incident lifecycle event. Never raises —
    a notification failure must never break incident management.
    """
    try:
        provider = get_notification_provider()

        if incident.severity == IncidentSeverity.CRITICAL and not incident.notified:
            sent = await provider.send_incident_alert(incident)
            if sent:
                incident.notified = True
                db.commit()
                logger.info(f"Incident #{incident.id} alert sent, marked as notified.")

        elif incident.status.value == "RESOLVED" and incident.notified:
            await provider.send_recovery_alert(incident)
            logger.info(f"Incident #{incident.id} recovery notice sent.")

    except Exception as e:
        logger.error(f"Notification failed for incident #{incident.id}: {e}")