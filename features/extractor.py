def extract_features(
    signing_frequency,
    device_change,
    location_change,
    activity_hour,
    failed_attempts,
    signature_count
):
    """
    Convert signing behavior into numerical features
    for the threat-detection system.
    """

    frequency_score = min(
        signing_frequency / 20,
        1.0
    )

    device_score = 1.0 if device_change else 0.0

    location_score = 1.0 if location_change else 0.0

    # Activity time is currently neutral.
    # A user's normal activity hours should eventually
    # be learned from their behavioral history rather
    # than assumed to be 09:00-18:00.

    time_score = 0.0

    failed_attempt_score = min(
        failed_attempts / 5,
        1.0
    )

    signature_count_score = min(
        signature_count / 20,
        1.0
    )

    return {
        "signing_frequency": frequency_score,
        "device_change": device_score,
        "location_change": location_score,
        "time_anomaly": time_score,
        "failed_attempts": failed_attempt_score,
        "signature_count": signature_count_score
    }