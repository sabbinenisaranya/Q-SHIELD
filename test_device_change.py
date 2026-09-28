from database.database import initialize_database, insert_event
from pipeline import QShieldPipeline


print("\n========================================")
print("     Q-SHIELD DEVICE CHANGE TEST")
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
# ADD PREVIOUS SIGNING ACTIVITY
# ============================================================

print("\nAdding previous signing activity...")


for i in range(5):

    insert_event(
        user_id="USER-001",
        document_id=f"device_test_{i}.pdf",
        timestamp=f"2026-09-22T19:{10 + i:02d}:00",
        device_id="DEVICE-001",
        ip_address="LOCAL",
        location="LOCAL",
        signature_valid=True,
        signing_frequency=1,
        device_change=0,
        location_change=0,
        activity_hour=19,
        failed_attempts=0,
        signature_count=i + 1,
        anomaly_score=0.1,
        quantum_score=0.05,
        threat_score=5,
        risk_level="LOW",
        threat_type="NONE"
    )


print("Previous activity added.")


# ============================================================
# SIMULATE NEW DEVICE
# ============================================================

print("\nSimulating a new device...")

pipeline.device_id = "DEVICE-002"

print("Current device:")
print(pipeline.device_id)


# ============================================================
# RUN AUTOMATIC ANALYSIS
# ============================================================

print("\nRunning automatic analysis...")


document = b"""
Q-Shield device change test document.
"""


result = pipeline.analyze(
    document=document
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n========================================")
print("        DEVICE CHANGE RESULT")
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
print("       DEVICE CHANGE TEST COMPLETE")
print("========================================")