from database.database import initialize_database, insert_event
from pipeline import QShieldPipeline


print("\n========================================")
print("   Q-SHIELD ISOLATED LOCATION TEST")
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


# ============================================================
# ADD PREVIOUS LEGITIMATE SIGNING EVENT
# ============================================================

print("\nAdding one legitimate signing event...")


insert_event(
    user_id="USER-001",
    document_id="location_test_previous.pdf",
    timestamp="2026-09-22T19:10:00",
    device_id="DEVICE-001",
    ip_address="LOCATION-A-IP",
    location="LOCATION-A",
    signature_valid=True,
    signing_frequency=1,
    device_change=0,
    location_change=0,
    activity_hour=19,
    failed_attempts=0,
    signature_count=1,
    anomaly_score=0.1,
    quantum_score=0.05,
    threat_score=5,
    risk_level="LOW",
    threat_type="NONE"
)


print("Previous location: LOCATION-A")


# ============================================================
# SIMULATE NEW LOCATION
# ============================================================

print("\nSimulating a new location...")


pipeline.device_id = "DEVICE-001"
pipeline.ip_address = "LOCATION-B-IP"
pipeline.location = "LOCATION-B"


print("Current location:")
print(pipeline.location)


# ============================================================
# RUN AUTOMATIC ANALYSIS
# ============================================================

print("\nRunning automatic analysis...")


document = b"""
Q-Shield location change test document.
"""


result = pipeline.analyze(
    document=document
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n========================================")
print("       LOCATION TEST RESULT")
print("========================================")


print("\nSIGNATURE VALID:")
print(
    result["signature_valid"]
)


# ============================================================
# BEHAVIOR
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
print("      LOCATION TEST COMPLETE")
print("========================================")