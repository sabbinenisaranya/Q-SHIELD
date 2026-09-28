import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "qshield.db"
)


def get_dashboard_data():
    """
    Read security events from the Q-SHIELD database
    and calculate dashboard statistics.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            threat_score,
            risk_level,
            threat_type,
            timestamp,
            document_id,
            device_id,
            ip_address,
            location
        FROM signature_events
        ORDER BY id ASC
        """
    )

    events = cursor.fetchall()

    connection.close()

    total_events = len(events)

    high_risk_events = sum(
        1
        for event in events
        if event[2] in ["HIGH", "CRITICAL"]
    )

    critical_events = sum(
        1
        for event in events
        if event[2] == "CRITICAL"
    )

    average_threat_score = (
        sum(event[1] for event in events)
        / total_events
        if total_events > 0
        else 0
    )

    risk_distribution = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0
    }

    threat_distribution = {}

    score_timeline = []

    alerts = []

    for event in events:

        (
            event_id,
            threat_score,
            risk_level,
            threat_type,
            timestamp,
            document_id,
            device_id,
            ip_address,
            location
        ) = event


        # ----------------------------------------------
        # RISK DISTRIBUTION
        # ----------------------------------------------

        if risk_level in risk_distribution:

            risk_distribution[risk_level] += 1


        # ----------------------------------------------
        # THREAT DISTRIBUTION
        # ----------------------------------------------

        if threat_type:

            threat_distribution[threat_type] = (
                threat_distribution.get(
                    threat_type,
                    0
                ) + 1
            )


        # ----------------------------------------------
        # SCORE TIMELINE
        # ----------------------------------------------

        score_timeline.append(
            {
                "timestamp": timestamp,
                "threat_score": threat_score
            }
        )


        # ----------------------------------------------
        # SECURITY ALERTS
        # ----------------------------------------------

        if risk_level in ["HIGH", "CRITICAL"]:

            alerts.append(
                {
                    "event_id": event_id,
                    "timestamp": timestamp,
                    "threat_score": threat_score,
                    "risk_level": risk_level,
                    "threat_type": threat_type,
                    "document_id": document_id,
                    "device_id": device_id,
                    "ip_address": ip_address,
                    "location": location
                }
            )


    # ----------------------------------------------
    # MOST RECENT ALERTS FIRST
    # ----------------------------------------------

    alerts.reverse()


    return {
        "total_events": total_events,

        "high_risk_events": high_risk_events,

        "critical_events": critical_events,

        "average_threat_score": round(
            average_threat_score,
            2
        ),

        "risk_distribution": risk_distribution,

        "threat_distribution": threat_distribution,

        "score_timeline": score_timeline,

        "alerts": alerts
    }