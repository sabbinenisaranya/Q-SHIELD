from database.database import initialize_database
from pipeline import QShieldPipeline


print("\n========================================")
print("        Q-SHIELD FULL PIPELINE")
print("========================================")


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# CREATE PIPELINE
# ============================================================

pipeline = QShieldPipeline()

pipeline.train_anomaly_detector()

print("\nML model trained.")


# ============================================================
# RUN AUTOMATIC BEHAVIORAL ANALYSIS
# ============================================================

print("\nRunning automatic behavioral analysis...")


document = b"""
Q-Shield full pipeline test document.
"""


result = pipeline.analyze(
    document=document
)


# ============================================================
# DIGITAL SIGNATURE
# ============================================================

print("\nSHA-256 HASH:")
print(
    result["document_hash"]
)


print("\nSIGNATURE VALID:")
print(
    result["signature_valid"]
)


# ============================================================
# USER / TELEMETRY INFORMATION
# ============================================================

print("\nUSER ID:")
print(
    result["user_id"]
)


print("\nTIMESTAMP:")
print(
    result["timestamp"]
)


print("\nDEVICE:")
print(
    result["device_id"]
)


print("\nIP ADDRESS:")
print(
    result["ip_address"]
)


print("\nLOCATION:")
print(
    result["location"]
)


# ============================================================
# AUTOMATIC BEHAVIOR
# ============================================================

behavior = result["behavior"]


print("\nAUTOMATIC BEHAVIOR:")


print(
    "Signing Frequency:",
    behavior["signing_frequency"]
)


print(
    "Device Change:",
    behavior["device_change"]
)


print(
    "Location Change:",
    behavior["location_change"]
)


print(
    "Activity Hour:",
    behavior["activity_hour"]
)


print(
    "Failed Attempts:",
    behavior["failed_attempts"]
)


print(
    "Signature Count:",
    behavior["signature_count"]
)


# ============================================================
# FEATURE EXTRACTION
# ============================================================

print("\nEXTRACTED FEATURES:")

features = result["features"]


for feature_name, feature_value in features.items():

    print(
        f"{feature_name}: "
        f"{feature_value:.3f}"
    )


# ============================================================
# ML ANOMALY DETECTION
# ============================================================

print("\nML ANOMALY SCORE:")

print(
    round(
        result["anomaly_score"],
        3
    )
)


print("\nML CLASSIFICATION:")

print(
    result["ml_classification"]
)


# ============================================================
# QUANTUM-INSPIRED ANALYSIS
# ============================================================

print("\nQUANTUM-INSPIRED WEIGHTS:")

for index, weight in enumerate(
    result["quantum_weights"]
):

    print(
        f"Feature {index + 1}: "
        f"{weight:.3f}"
    )


print("\nQUANTUM-INSPIRED SCORE:")

print(
    round(
        result["quantum_score"],
        3
    )
)


# ============================================================
# THREAT ASSESSMENT
# ============================================================

print("\nFINAL THREAT SCORE:")

print(
    result["threat_score"]
)


print("\nRISK LEVEL:")

print(
    result["risk_level"]
)


print("\nTHREAT TYPE:")

print(
    result["threat_type"]
)


# ============================================================
# TEST COMPLETE
# ============================================================

print("\n========================================")
print("       FULL PIPELINE TEST COMPLETE")
print("========================================")