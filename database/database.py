import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATH
# ============================================================

DATABASE_PATH = Path(__file__).parent / "qshield.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create a connection to the Q-Shield SQLite database.
    """
    connection = sqlite3.connect(
        DATABASE_PATH
    )

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Create the signature_events table
    if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS signature_events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT,

            document_id TEXT,

            timestamp TEXT,

            device_id TEXT,

            ip_address TEXT,

            location TEXT,

            signature_valid INTEGER,

            signing_frequency REAL,

            device_change INTEGER,

            location_change INTEGER,

            activity_hour INTEGER,

            failed_attempts INTEGER,

            signature_count INTEGER,

            anomaly_score REAL,

            quantum_score REAL,

            threat_score REAL,

            risk_level TEXT,

            threat_type TEXT

        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# INSERT SECURITY EVENT
# ============================================================

def insert_event(
    user_id,
    document_id,
    timestamp,
    device_id,
    ip_address,
    location,
    signature_valid,
    signing_frequency=0,
    device_change=0,
    location_change=0,
    activity_hour=0,
    failed_attempts=0,
    signature_count=0,
    anomaly_score=0,
    quantum_score=0,
    threat_score=0,
    risk_level="UNKNOWN",
    threat_type="NONE"
):
    """
    Store one Q-Shield security event
    in the SQLite database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO signature_events (

            user_id,
            document_id,
            timestamp,
            device_id,
            ip_address,
            location,
            signature_valid,
            signing_frequency,
            device_change,
            location_change,
            activity_hour,
            failed_attempts,
            signature_count,
            anomaly_score,
            quantum_score,
            threat_score,
            risk_level,
            threat_type

        )

        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,

        (
            user_id,
            document_id,
            timestamp,
            device_id,
            ip_address,
            location,
            int(signature_valid),
            signing_frequency,
            device_change,
            location_change,
            activity_hour,
            failed_attempts,
            signature_count,
            anomaly_score,
            quantum_score,
            threat_score,
            risk_level,
            threat_type
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# GET SECURITY EVENTS
# ============================================================

def get_events():
    """
    Retrieve all security events from the database.

    Events are returned with the newest event first.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            id,
            user_id,
            document_id,
            timestamp,
            device_id,
            ip_address,
            location,
            signature_valid,
            anomaly_score,
            quantum_score,
            threat_score,
            risk_level,
            threat_type

        FROM signature_events

        ORDER BY id DESC
        """
    )

    events = cursor.fetchall()

    connection.close()

    return events