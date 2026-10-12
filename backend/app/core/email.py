import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_otp_email(to_email: str, otp: str, purpose: str = "verification") -> bool:
    """
    Pluggable email provider for OTP delivery.
    In development, prints to server console if SMTP is not configured.
    In production, strictly requires working SMTP and never prints or logs OTP.
    """
    subject = f"Your {settings.APP_NAME} Verification Code"
    content = (
        f"Hello,\n\n"
        f"Your one-time verification code for {settings.APP_NAME} ({purpose}) is:\n\n"
        f"    {otp}\n\n"
        f"This code will expire in 10 minutes.\n"
        f"If you did not request this code, please ignore this email.\n\n"
        f"— The {settings.APP_NAME} Team"
    )

    if settings.SMTP_HOST:
        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
            msg["To"] = to_email
            msg.set_content(content)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                server.starttls()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            if settings.is_development:
                print(f"[Email Error] Failed to send via SMTP: {e}")
                # Fallback to dev console in development only
                _print_dev_otp(to_email, otp, purpose)
                return True
            raise RuntimeError(f"Email delivery failed in production: {e}")

    # No SMTP configured
    if settings.is_development:
        _print_dev_otp(to_email, otp, purpose)
        return True
    else:
        raise RuntimeError("SMTP configuration missing in production environment. Refusing to process OTP.")

def _print_dev_otp(to_email: str, otp: str, purpose: str):
    print("\n" + "=" * 55)
    print(f" [DEV MODE OTP DELIVERY] — NOT FOR PRODUCTION")
    print(f" To:      {to_email}")
    print(f" Purpose: {purpose}")
    print(f" OTP:     {otp}")
    print(f" Valid:   10 minutes")
    print("=" * 55 + "\n")
