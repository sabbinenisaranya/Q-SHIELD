import database.database as database
from pipeline import QShieldPipeline


print("\n========================================")
print("   Q-SHIELD ISOLATED DEVICE TEST")
print("========================================")


# Create a separate test database
original_database_path = database.DATABASE_PATH

database.DATABASE_PATH = (
    original_database_path.parent
    / "device_test.db"
)


# Delete the old test database if it exists
if database.DATABASE_PATH.exists():
    database.DATABASE_PATH.unlink()


# Create the clean test database
database.initialize_database()


# Create Q-Shield pipeline
pipeline = QShieldPipeline()

pipeline.train_anomaly_detector()


print("\nAdding one legitimate signing event...")


# Previous signing was done on DEVICE-001
database.insert_event(
    user_id="USER-001",
    document_id="legitimate_document.pdf",
    timestamp="2026-09-22T19:00:00",
    device_id="DEVICE-001",
    ip_address="LOCAL",
    location="LOCAL",
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


print("Previous device: DEVICE-001")


print("\nSimulating a new device...")


# The new signing happens on DEVICE-002
pipeline.device_id = "DEVICE-002"


print("Current device:", pipeline.device_id)


print("\nRunning automatic analysis...")


document = b"""
Q-Shield isolated device change test.
"""


result = pipeline.analyze(
    document=document
)


print("\n========================================")
print("       ISOLATED TEST RESULT")
print("========================================")


print("\nSIGNATURE VALID:")
print(result["signature_valid"])


print("\nAUTOMATIC BEHAVIOR:")

print(
    "Signing Frequency:",
    result["signing_frequency"]
)

print(
    "Device Change:",
    result["device_change"]
)

print(
    "Location Change:",
    result["location_change"]
)

print(
    "Failed Attempts:",
    result["failed_attempts"]
)

print(
    "Signature Count:",
    result["signature_count"]
)


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


print("\nQUANTUM-INSPIRED SCORE:")
print(
    round(
        result["quantum_score"],
        3
    )
)


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


print("\n========================================")
print("    ISOLATED DEVICE TEST COMPLETE")
print("========================================")