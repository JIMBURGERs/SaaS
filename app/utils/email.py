import os
import smtplib
from email.message import EmailMessage


ENV = os.getenv("ENV", "dev")
EMAIL_SEND_IN_DEV = os.getenv("EMAIL_SEND_IN_DEV", "false").lower() in ("1", "true", "yes", "y")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:3000")


def _should_send_email() -> bool:
    return ENV == "prod" or EMAIL_SEND_IN_DEV


def _send_email(msg: EmailMessage, to_email: str):
    if not _should_send_email():
        print(f"[EMAIL] skip (ENV={ENV}) -> {to_email}")
        return

    if not SMTP_USER or not SMTP_PASSWORD:
        print("[EMAIL] SMTP credentials missing")
        return

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"[EMAIL] sent -> {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] {type(e).__name__}: {e}")


def send_registration_email(to_email: str, first_name: str):
    msg = EmailMessage()
    msg["Subject"] = "Welcome to Playntel"
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.set_content(
        f"""Hi {first_name},

Your account has been successfully created.

You can now log in to Playntel.
Some activity features may remain limited until verification is completed.

Team Playntel
"""
    )
    _send_email(msg, to_email)


def send_email_verification_email(to_email: str, first_name: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Playntel Email Verification Code"
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.set_content(
        f"""Hi {first_name},

Your Playntel email verification code is:

{code}

If you did not request this, please ignore this email.

Team Playntel
"""
    )
    _send_email(msg, to_email)


def send_password_reset_email(to_email: str, reset_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Playntel Password Reset"
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.set_content(
        f"""Hi,

We received a request to reset your password.

Reset link:
{reset_link}

If you did not request this, please ignore this email.

Team Playntel
"""
    )
    _send_email(msg, to_email)


def send_password_changed_email(to_email: str):
    msg = EmailMessage()
    msg["Subject"] = "Playntel Password Changed"
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.set_content(
        """Hi,

Your password has been successfully changed.

If you did NOT perform this action, please reset your password immediately or contact support.

Team Playntel
"""
    )
    _send_email(msg, to_email)


def send_login_alert_email(to_email: str, first_name: str | None = None):
    msg = EmailMessage()
    msg["Subject"] = "New login detected"
    msg["From"] = SMTP_FROM
    msg["To"] = to_email

    name = first_name or "there"

    msg.set_content(
        f"""Hi {name},

A new login to your Playntel account was detected.

If this was you, no action is needed.
If not, please reset your password immediately.

Team Playntel
"""
    )
    _send_email(msg, to_email)