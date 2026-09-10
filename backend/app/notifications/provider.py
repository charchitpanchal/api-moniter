import logging
from abc import ABC, abstractmethod
from app.models.incident import Incident

logger = logging.getLogger("notifications.provider")


class NotificationProvider(ABC):
    """
    Abstract interface — same pattern as Day 9's LLMProvider.
    Any real delivery mechanism (email via SNS, Slack, SMS) implements this.
    """

    @abstractmethod
    async def send_incident_alert(self, incident: Incident) -> bool:
        """Returns True if the notification was sent successfully."""
        raise NotImplementedError

    @abstractmethod
    async def send_recovery_alert(self, incident: Incident) -> bool:
        raise NotImplementedError


class ConsoleNotifier(NotificationProvider):
    """
    Stand-in provider used until AWS SNS is wired in during the final
    deployment phase. Logs exactly what a real notification would contain,
    so the notification LOGIC (when/whether to send) is fully built and
    testable right now without any AWS dependency.
    """

    async def send_incident_alert(self, incident: Incident) -> bool:
        api = incident.api
        logger.warning(
            f"\n"
            f"========================================\n"
            f"🚨 [WOULD SEND EMAIL] INCIDENT ALERT\n"
            f"----------------------------------------\n"
            f"API: {api.name} ({api.url})\n"
            f"Severity: {incident.severity}\n"
            f"Failure Count: {incident.failure_count}\n"
            f"Last Error: {incident.last_error}\n"
            f"Started At: {incident.started_at}\n"
            f"========================================\n"
        )
        return True

    async def send_recovery_alert(self, incident: Incident) -> bool:
        api = incident.api
        logger.info(
            f"\n"
            f"========================================\n"
            f"✅ [WOULD SEND EMAIL] RECOVERY NOTICE\n"
            f"----------------------------------------\n"
            f"API: {api.name} ({api.url})\n"
            f"Incident Duration: {incident.resolution_time}s\n"
            f"Resolved At: {incident.resolved_at}\n"
            f"========================================\n"
        )
        return True


def get_notification_provider() -> NotificationProvider:
    """
    Factory function — same pattern as Day 9's get_provider().
    """
    from app.core.config import settings

    provider_name = settings.notification_provider.lower()

    if provider_name == "console":
        return ConsoleNotifier()
    else:
        raise ValueError(f"Unsupported NOTIFICATION_PROVIDER: {provider_name}")