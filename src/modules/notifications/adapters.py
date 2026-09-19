from fastapi import BackgroundTasks

from src.core.config import AppConfig, SMTPConfig

from .service import send_verification_email


class FastAPIEmailSender:
    def __init__(self, bg_tasks: BackgroundTasks, app_config: AppConfig, smtp_config: SMTPConfig):
        self.bg_tasks = bg_tasks
        self.app_config = app_config
        self.smtp_config = smtp_config

    def send_verification(self, email: str, token: str) -> None:
        url = f"{self.app_config.base_url}/api/auth/verify-email?token={token}"
        self.bg_tasks.add_task(send_verification_email, email, url, self.smtp_config)
