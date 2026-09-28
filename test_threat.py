from threat.scorer import calculate_threat_score


print("\n========================================")
print("       Q-SHIELD THREAT SCORE TEST")
print("========================================")


# ============================================================
# TEST INPUTS
# ============================================================

signature_valid = True

anomaly_score = 0.75

quantum_score = 0.85


# ============================================================
# BEHAVIORAL FEATURES
# ============================================================

features = {

    "signing_frequency": 0.50,

    "device_change": 1.00,

    "location_change": 0.00,

    "time_anomaly": 0.00,

    "failed_attempts": 0.20,

    "signature_count": 0.50

}


# ============================================================
# CALCULATE THREAT SCORE
# ============================================================

threat_score, risk_level = calculate_threat_score(

    signature_valid=signature_valid,

    anomaly_score=anomaly_score,

    quantum_score=quantum_score,

    features=features

)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\nSignature Valid:")
print(signature_valid)


print("\nAnomaly Score:")
print(anomaly_score)


print("\nQuantum-Inspired Score:")
print(quantum_score)


print("\nBehavioral Features:")

for feature_name, feature_value in features.items():

    print(
        f"{feature_name}: "
        f"{feature_value}"
    )


print("\nFinal Threat Score:")
print(threat_score)


print("\nRisk Level:")
print(risk_level)


# ============================================================
# BASIC VALIDATION
# ============================================================

if not 0 <= threat_score <= 100:

    raise RuntimeError(
        "Threat score is outside the valid 0-100 range."
    )


if risk_level not in [
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL"
]:

    raise RuntimeError(
        "Invalid risk level returned."
    )


print("\n========================================")
print("       THREAT SCORE TEST PASSED")
print("========================================")