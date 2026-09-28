from database.database import initialize_database, insert_event
from pipeline import QShieldPipeline


print("\n========================================")
print("     Q-SHIELD BEHAVIOR TEST")
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


# Add 10 previous legitimate signing events
for i in range(10):

    insert_event(
        user_id="USER-001",
        document_id=f"previous_document_{i}.pdf",
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
# RUN AUTOMATIC ANALYSIS
# ============================================================

print("\nRunning new automatic analysis...")


document = b"""
Q-Shield suspicious behavior test.
"""


result = pipeline.analyze(
    document=document
)


# ============================================================
# DISPLAY CURRENT ANALYSIS
# ============================================================

print("\n========================================")
print("        CURRENT ANALYSIS")
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
print("       BEHAVIOR TEST COMPLETE")
print("========================================")