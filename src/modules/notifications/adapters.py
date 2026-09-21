from fastapi import BackgroundTasks

from src.core.config import SMTPConfig

from .service import send_verification_email


class FastAPIEmailSender:
    def __init__(self, bg_tasks: BackgroundTasks, smtp_config: SMTPConfig):
        self.bg_tasks = bg_tasks
        self.smtp_config = smtp_config

    def send_verification(self, email: str, link: str) -> None:
        self.bg_tasks.add_task(send_verification_email, email, link, self.smtp_config)
