from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.config import settings
from app.core.security import hash_password, verify_password, generate_otp, hash_otp, generate_session_token
from app.core.email import send_otp_email
from app.core.deps import get_current_user
from app.core.rate_limit import enforce_rate_limit
from app.models import User, Session as UserSession, OTPCode
from app.schemas.auth import (
    RegisterRequest,
    VerifyOTPRequest,
    ResendOTPRequest,
    LoginRequest,
    AuthResponse,
    UserResponse
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

OTP_EXPIRY_MINUTES = 10
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_COOLDOWN_SECONDS = 60

@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request, "register", max_hits=6, window_seconds=60)
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == req.email).first()
    if existing_user and existing_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please log in."
        )

    # Check cooldown for recent OTP
    recent_otp = db.query(OTPCode).filter(
        OTPCode.email == req.email,
        OTPCode.purpose == "register",
        OTPCode.verified == False
    ).order_by(OTPCode.created_at.desc()).first()

    if recent_otp:
        time_since = (datetime.utcnow() - recent_otp.created_at).total_seconds()
        if time_since < OTP_RESEND_COOLDOWN_SECONDS:
            remaining = int(OTP_RESEND_COOLDOWN_SECONDS - time_since)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Please wait {remaining} seconds before requesting another verification code."
            )

    # Hash password using Argon2
    pw_hash = hash_password(req.password)

    if existing_user:
        # Update existing unverified user
        existing_user.username = req.username
        existing_user.password_hash = pw_hash
        existing_user.year = req.year
        existing_user.degree = req.degree
        existing_user.branch = req.branch
        db.commit()
    else:
        new_user = User(
            username=req.username,
            email=req.email,
            password_hash=pw_hash,
            year=req.year,
            degree=req.degree,
            branch=req.branch,
            email_verified=False
        )
        db.add(new_user)
        db.commit()

    # Generate and save OTP
    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    expires = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    otp_record = OTPCode(
        email=req.email,
        otp_hash=hashed_otp,
        purpose="register",
        attempts=0,
        expires_at=expires,
        verified=False
    )
    db.add(otp_record)
    db.commit()

    # Send OTP
    send_otp_email(req.email, otp, purpose="account registration")

    return AuthResponse(
        success=True,
        message="Registration initiated. A 6-digit verification code has been sent to your email."
    )


@router.post("/verify-otp", response_model=AuthResponse)
def verify_otp(req: VerifyOTPRequest, response: Response, request: Request, db: Session = Depends(get_db)):
    otp_record = db.query(OTPCode).filter(
        OTPCode.email == req.email,
        OTPCode.verified == False
    ).order_by(OTPCode.created_at.desc()).first()

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending verification code found for this email. Please request a new one."
        )

    # Check attempt limit
    if otp_record.attempts >= OTP_MAX_ATTEMPTS:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum verification attempts exceeded. Please request a new code."
        )

    # Check expiration
    if otp_record.expires_at < datetime.utcnow():
        db.delete(otp_record)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired. Please request a new code."
        )

    # Verify hash
    if hash_otp(req.otp) != otp_record.otp_hash:
        otp_record.attempts += 1
        db.commit()
        remaining = OTP_MAX_ATTEMPTS - otp_record.attempts
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid verification code. {remaining} attempt(s) remaining."
        )

    # Mark OTP as verified (single-use)
    otp_record.verified = True

    # Mark user as verified
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")

    user.email_verified = True

    # Create server-side session
    token = generate_session_token()
    session_expires = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRE_DAYS)

    session_record = UserSession(
        user_id=user.id,
        token=token,
        expires_at=session_expires,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host if request.client else None
    )
    db.add(session_record)
    db.commit()
    db.refresh(user)

    # Set httpOnly SameSite cookie
    response.set_cookie(
        key="sf_session",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.is_production,
        max_age=settings.SESSION_EXPIRE_DAYS * 86400,
        path="/"
    )

    return AuthResponse(
        success=True,
        message="Email successfully verified. Welcome to SkillForage AI!",
        user=UserResponse.model_validate(user),
    )


@router.post("/resend-otp", response_model=AuthResponse)
def resend_otp(req: ResendOTPRequest, request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request, "resend-otp", max_hits=5, window_seconds=60)
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    # Check cooldown
    recent_otp = db.query(OTPCode).filter(
        OTPCode.email == req.email,
        OTPCode.verified == False
    ).order_by(OTPCode.created_at.desc()).first()

    if recent_otp:
        time_since = (datetime.utcnow() - recent_otp.created_at).total_seconds()
        if time_since < OTP_RESEND_COOLDOWN_SECONDS:
            remaining = int(OTP_RESEND_COOLDOWN_SECONDS - time_since)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Please wait {remaining} seconds before requesting a new code."
            )

    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    expires = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    otp_record = OTPCode(
        email=req.email,
        otp_hash=hashed_otp,
        purpose="register" if not user.email_verified else "verification",
        attempts=0,
        expires_at=expires,
        verified=False
    )
    db.add(otp_record)
    db.commit()

    send_otp_email(req.email, otp, purpose="verification code resend")

    return AuthResponse(
        success=True,
        message="A new 6-digit verification code has been sent to your email."
    )


@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, response: Response, request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request, "login", max_hits=10, window_seconds=60)
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not user.email_verified:
        # Re-send verification code
        otp = generate_otp()
        hashed_otp = hash_otp(otp)
        expires = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

        otp_record = OTPCode(
            email=req.email,
            otp_hash=hashed_otp,
            purpose="register",
            attempts=0,
            expires_at=expires,
            verified=False
        )
        db.add(otp_record)
        db.commit()
        send_otp_email(req.email, otp, purpose="account verification")

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email address not verified. A new verification code has been sent to your email."
        )

    # Create server-side session
    token = generate_session_token()
    session_expires = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRE_DAYS)

    session_record = UserSession(
        user_id=user.id,
        token=token,
        expires_at=session_expires,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host if request.client else None
    )
    db.add(session_record)
    db.commit()

    # Set httpOnly cookie
    response.set_cookie(
        key="sf_session",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.is_production,
        max_age=settings.SESSION_EXPIRE_DAYS * 86400,
        path="/"
    )

    return AuthResponse(
        success=True,
        message="Login successful.",
        user=UserResponse.model_validate(user),
    )


@router.post("/logout", response_model=AuthResponse)
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("sf_session")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()

    if token:
        db.query(UserSession).filter(UserSession.token == token).delete()
        db.commit()

    response.delete_cookie(key="sf_session", path="/")

    return AuthResponse(
        success=True,
        message="You have been safely logged out."
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(user: User = Depends(get_current_user)):
    return user
