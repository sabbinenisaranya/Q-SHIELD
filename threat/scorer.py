def calculate_threat_score(
    signature_valid,
    anomaly_score,
    quantum_score,
    features
):
    """
    Calculate the final Q-Shield threat score.

    The score combines:
    - Digital signature integrity
    - ML anomaly detection
    - Quantum-inspired signal
    - Individual behavioral features

    Returns:
        threat_score: 0-100
        risk_level: LOW / MEDIUM / HIGH / CRITICAL
    """

    # --------------------------------------------------
    # 1. Signature integrity
    # --------------------------------------------------

    if signature_valid:
        signature_component = 0
    else:
        signature_component = 40


    # --------------------------------------------------
    # 2. Behavioral components
    # --------------------------------------------------

    frequency_component = (
        features["signing_frequency"] * 15
    )

    device_component = (
        features["device_change"] * 20
    )

    location_component = (
        features["location_change"] * 20
    )

    failed_attempt_component = (
        features["failed_attempts"] * 15
    )

    signature_count_component = (
        features["signature_count"] * 5
    )


    # --------------------------------------------------
    # 3. Machine-learning component
    # --------------------------------------------------

    anomaly_component = (
        anomaly_score * 20
    )


    # --------------------------------------------------
    # 4. Quantum-inspired supporting component
    # --------------------------------------------------

    quantum_component = (
        quantum_score * 5
    )


    # --------------------------------------------------
    # 5. Final score
    # --------------------------------------------------

    threat_score = (
        signature_component
        + frequency_component
        + device_component
        + location_component
        + failed_attempt_component
        + signature_count_component
        + anomaly_component
        + quantum_component
    )


    # Keep the result between 0 and 100.
    threat_score = max(
        0,
        min(
            100,
            threat_score
        )
    )


    # --------------------------------------------------
    # 6. Risk level
    # --------------------------------------------------

    if threat_score <= 30:
        risk_level = "LOW"

    elif threat_score <= 60:
        risk_level = "MEDIUM"

    elif threat_score <= 80:
        risk_level = "HIGH"

    else:
        risk_level = "CRITICAL"


    return (
        round(threat_score, 2),
        risk_level
    )