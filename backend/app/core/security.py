import hashlib
import secrets
import string
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=1,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    """Hash password using Argon2id."""
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against Argon2 hash."""
    try:
        return ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False

def generate_otp() -> str:
    """Generate cryptographically secure 6-digit OTP."""
    digits = string.digits
    return "".join(secrets.choice(digits) for _ in range(6))

def hash_otp(otp: str) -> str:
    """Hash OTP with SHA-256 for secure storage."""
    return hashlib.sha256(otp.encode("utf-8")).hexdigest()

def generate_session_token() -> str:
    """Generate 64-character cryptographically random session token."""
    return secrets.token_hex(32)
