import logging
import smtplib
from email.mime.text import MIMEText
from abc import ABC, abstractmethod
from app.models.incident import Incident
from app.core.config import settings

logger = logging.getLogger("notifications.provider")


class NotificationProvider(ABC):
    @abstractmethod
    async def send_incident_alert(self, incident: Incident) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def send_recovery_alert(self, incident: Incident) -> bool:
        raise NotImplementedError


class ConsoleNotifier(NotificationProvider):
    async def send_incident_alert(self, incident: Incident) -> bool:
        api = incident.api
        logger.warning(
            f"INCIDENT ALERT - API: {api.name} ({api.url}) "
            f"Severity: {incident.severity} "
            f"Failure Count: {incident.failure_count} "
            f"Last Error: {incident.last_error}"
        )
        return True

    async def send_recovery_alert(self, incident: Incident) -> bool:
        api = incident.api
        logger.info(
            f"RECOVERY - API: {api.name} "
            f"Duration: {incident.resolution_time}s"
        )
        return True


class EmailNotifier(NotificationProvider):
    def _send_email(self, subject: str, body: str) -> bool:
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = settings.smtp_user
            msg["To"] = settings.notify_email_to

            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_user, settings.notify_email_to, msg.as_string())
            return True
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False

    async def send_incident_alert(self, incident: Incident) -> bool:
        api = incident.api
        subject = f"CRITICAL Incident - {api.name}"
        body = (
            f"API: {api.name} ({api.url})\n"
            f"Severity: {incident.severity}\n"
            f"Failure Count: {incident.failure_count}\n"
            f"Last Error: {incident.last_error}\n"
            f"Started At: {incident.started_at}"
        )
        return self._send_email(subject, body)

    async def send_recovery_alert(self, incident: Incident) -> bool:
        api = incident.api
        subject = f"Recovered - {api.name}"
        body = (
            f"API: {api.name}\n"
            f"Downtime: {incident.resolution_time}s\n"
            f"Resolved At: {incident.resolved_at}"
        )
        return self._send_email(subject, body)


def get_notification_provider() -> NotificationProvider:
    provider_name = settings.notification_provider.lower()
    if provider_name == "console":
        return ConsoleNotifier()
    elif provider_name == "email":
        return EmailNotifier()
    else:
        raise ValueError(f"Unsupported NOTIFICATION_PROVIDER: {provider_name}")