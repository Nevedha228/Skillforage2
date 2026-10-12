from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import User, Session as UserSession

def get_session_token_from_request(request: Request) -> Optional[str]:
    # 1. First check httpOnly cookie
    token = request.cookies.get("sf_session")
    if token:
        return token
    # 2. Check Authorization Bearer header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    return None

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    token = get_session_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    session_record = db.query(UserSession).filter(UserSession.token == token).first()
    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if session_record.expires_at < datetime.utcnow():
        # Clean up expired session
        db.delete(session_record)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == session_record.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with session not found.",
        )

    return user

def get_optional_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    try:
        return get_current_user(request, db)
    except HTTPException:
        return None
