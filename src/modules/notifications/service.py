from email.message import EmailMessage

import aiosmtplib

from src.core.config import SMTPConfig


async def send_verification_email(to_email: str, link: str, config: SMTPConfig) -> None:
    message = EmailMessage()
    message["From"] = config.from_email
    message["To"] = to_email
    message["Subject"] = "Email Verification"
    message.set_content(f"To verify your account, follow the link: {link}")

    await aiosmtplib.send(
        message,
        hostname=config.host,
        port=config.port,
        username=config.user,
        password=config.password,
        use_tls=config.use_tls,
    )
