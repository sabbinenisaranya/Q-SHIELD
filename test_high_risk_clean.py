from database.database import initialize_database, insert_event
from pipeline import QShieldPipeline


print("\n========================================")
print("      Q-SHIELD HIGH-RISK TEST")
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
# CREATE SUSPICIOUS HISTORICAL ACTIVITY
# ============================================================

print("\nCreating suspicious historical activity...")


for i in range(12):

    insert_event(
        user_id="USER-001",
        document_id="Q_SHIELD_High_Risk_Test_Document.pdf",
        timestamp=f"2026-09-22T20:01:{i:02d}",
        device_id="DEVICE-001",
        ip_address="LOCATION-A-IP",
        location="LOCATION-A",
        signature_valid=True,
        signing_frequency=20,
        device_change=0,
        location_change=0,
        activity_hour=20,
        failed_attempts=0,
        signature_count=i + 1,
        anomaly_score=0.9,
        quantum_score=0.9,
        threat_score=70,
        risk_level="HIGH",
        threat_type="VALID_SIGNATURE_MISUSE"
    )


print("12 previous abnormal events created.")


# ============================================================
# SIMULATE SUSPICIOUS CURRENT ACTIVITY
# ============================================================

pipeline.device_id = "DEVICE-002"
pipeline.ip_address = "LOCATION-B-IP"
pipeline.location = "LOCATION-B"


print("\nSimulating current signing from:")
print("Device:   ", pipeline.device_id)
print("Location: ", pipeline.location)


# ============================================================
# RUN AUTOMATIC ANALYSIS
# ============================================================

print("\nRunning automatic analysis...")


document = b"""
Q-Shield high-risk behavioral analysis test document.
"""


result = pipeline.analyze(
    document=document
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n========================================")
print("          HIGH-RISK RESULT")
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
print("       HIGH-RISK TEST COMPLETE")
print("========================================")