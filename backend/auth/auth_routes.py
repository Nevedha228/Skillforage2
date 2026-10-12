from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

import random
import smtplib
import os

from email.message import EmailMessage

from .database import (
    save_otp,
    verify_otp,
    create_user,
    get_user_by_email
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRequest(BaseModel):

    username: str
    email: EmailStr
    year: str
    degree: str
    branch: str


class OTPRequest(BaseModel):

    email: EmailStr


class VerifyRegisterRequest(BaseModel):

    username: str
    email: EmailStr
    year: str
    degree: str
    branch: str
    otp: str


class VerifyLoginRequest(BaseModel):

    email: EmailStr
    otp: str


# ============================================================
# EMAIL OTP
# ============================================================

def generate_otp():

    return str(
        random.randint(100000, 999999)
    )


def send_email_otp(email, otp):

    smtp_host = os.getenv(
        "SMTP_HOST",
        ""
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    smtp_email = os.getenv(
        "SMTP_EMAIL",
        ""
    )

    smtp_password = os.getenv(
        "SMTP_PASSWORD",
        ""
    )

    # Development mode
    if not smtp_host:

        print(
            "\n===================================="
        )

        print(
            "SKILLFORGE DEVELOPMENT OTP"
        )

        print(
            "Email:",
            email
        )

        print(
            "OTP:",
            otp
        )

        print(
            "====================================\n"
        )

        return True

    message = EmailMessage()

    message["Subject"] = "SkillForage Email Verification OTP"

    message["From"] = smtp_email

    message["To"] = email

    message.set_content(
        f"""
Hello,

Your SkillForage verification OTP is:

{otp}

This OTP is valid for 10 minutes.

If you did not request this code, please ignore this email.

SkillForage AI
"""
    )

    with smtplib.SMTP(
        smtp_host,
        smtp_port
    ) as server:

        server.starttls()

        server.login(
            smtp_email,
            smtp_password
        )

        server.send_message(
            message
        )

    return True


# ============================================================
# REGISTER — SEND OTP
# ============================================================

@router.post("/register/send-otp")
def register_send_otp(
    request: RegisterRequest
):

    existing_user = get_user_by_email(
        request.email
    )

    if existing_user:

        return {
            "success": False,
            "message": "Email is already registered."
        }

    otp = generate_otp()

    save_otp(
        email=request.email,
        otp=otp,
        purpose="register"
    )

    send_email_otp(
        request.email,
        otp
    )

    return {
        "success": True,
        "message": "OTP sent successfully."
    }


# ============================================================
# REGISTER — VERIFY OTP
# ============================================================

@router.post("/register/verify-otp")
def register_verify_otp(
    request: VerifyRegisterRequest
):

    valid = verify_otp(
        email=request.email,
        otp=request.otp,
        purpose="register"
    )

    if not valid:

        return {
            "success": False,
            "message": "Invalid or expired OTP."
        }

    existing_user = get_user_by_email(
        request.email
    )

    if existing_user:

        return {
            "success": False,
            "message": "Email is already registered."
        }

    user_id = create_user(
        username=request.username,
        email=request.email,
        year=request.year,
        degree=request.degree,
        branch=request.branch
    )

    return {
        "success": True,
        "message": "Registration completed successfully.",
        "user_id": user_id
    }


# ============================================================
# LOGIN — SEND OTP
# ============================================================

@router.post("/login/send-otp")
def login_send_otp(
    request: OTPRequest
):

    user = get_user_by_email(
        request.email
    )

    if not user:

        return {
            "success": False,
            "message": "No account found with this email."
        }

    otp = generate_otp()

    save_otp(
        email=request.email,
        otp=otp,
        purpose="login"
    )

    send_email_otp(
        request.email,
        otp
    )

    return {
        "success": True,
        "message": "Login OTP sent successfully."
    }


# ============================================================
# LOGIN — VERIFY OTP
# ============================================================

@router.post("/login/verify-otp")
def login_verify_otp(
    request: VerifyLoginRequest
):

    valid = verify_otp(
        email=request.email,
        otp=request.otp,
        purpose="login"
    )

    if not valid:

        return {
            "success": False,
            "message": "Invalid or expired OTP."
        }

    user = get_user_by_email(
        request.email
    )

    if not user:

        return {
            "success": False,
            "message": "User account not found."
        }

    return {
        "success": True,
        "message": "Login successful.",
        "user": user
    }