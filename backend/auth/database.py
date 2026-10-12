import sqlite3
import os
import hashlib
from datetime import datetime, timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "skillforge_users.db"
)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            year TEXT NOT NULL,
            degree TEXT NOT NULL,
            branch TEXT NOT NULL,
            email_verified INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS otp_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp_hash TEXT NOT NULL,
            purpose TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            verified INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()


def hash_otp(otp):

    return hashlib.sha256(
        otp.encode("utf-8")
    ).hexdigest()


def save_otp(email, otp, purpose):

    connection = get_connection()

    cursor = connection.cursor()

    otp_hash = hash_otp(otp)

    expires_at = (
        datetime.utcnow() + timedelta(minutes=10)
    ).isoformat()

    created_at = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO otp_codes
        (
            email,
            otp_hash,
            purpose,
            expires_at,
            verified,
            created_at
        )
        VALUES (?, ?, ?, ?, 0, ?)
        """,
        (
            email,
            otp_hash,
            purpose,
            expires_at,
            created_at
        )
    )

    connection.commit()

    connection.close()


def verify_otp(email, otp, purpose):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM otp_codes
        WHERE email = ?
        AND purpose = ?
        AND verified = 0
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            email,
            purpose
        )
    )

    record = cursor.fetchone()

    if not record:

        connection.close()

        return False

    expires_at = datetime.fromisoformat(
        record["expires_at"]
    )

    if datetime.utcnow() > expires_at:

        connection.close()

        return False

    entered_hash = hash_otp(otp)

    if entered_hash != record["otp_hash"]:

        connection.close()

        return False

    cursor.execute(
        """
        UPDATE otp_codes
        SET verified = 1
        WHERE id = ?
        """,
        (record["id"],)
    )

    connection.commit()

    connection.close()

    return True


def create_user(
    username,
    email,
    year,
    degree,
    branch
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            email,
            year,
            degree,
            branch,
            email_verified,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, 1, ?)
        """,
        (
            username,
            email,
            year,
            degree,
            branch,
            created_at
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if user:

        return dict(user)

    return None