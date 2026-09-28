from pathlib import Path

from reports.report_generator import generate_security_report


print()
print("Q-SHIELD PDF REPORT GENERATOR TEST")
print("=" * 45)


sample_result = {
    "user_id": "USER-001",

    "document_hash": (
        "SAMPLE_HASH_123456789"
    ),

    "signature_valid": True,

    "timestamp": (
        "2026-09-27T17:00:00"
    ),

    "device_id": (
        "DEVICE-TEST001"
    ),

    "ip_address": (
        "127.0.0.1"
    ),

    "location": (
        "Test Location"
    ),

    "anomaly_score": 0.72,

    "ml_classification": (
        "ANOMALY"
    ),

    "quantum_score": 0.91,

    "quantum_weights": [
        0.18,
        0.22,
        0.17,
        0.15,
        0.16,
        0.12
    ],

    "threat_score": 54.32,

    "risk_level": (
        "MEDIUM"
    ),

    "threat_type": (
        "VALID_SIGNATURE_MISUSE"
    ),

    "behavior": {
        "signing_frequency": 0.75,
        "device_change": 1,
        "location_change": 0,
        "activity_hour": 17,
        "failed_attempts": 1,
        "signature_count": 5
    }
}


# ============================================================
# GENERATE REPORT
# ============================================================

report_path = generate_security_report(
    sample_result,
    "sample_test_document.pdf"
)


# ============================================================
# VERIFY REPORT
# ============================================================

print()
print("Report generated successfully.")

print()
print("Report path:")
print(report_path)

print()
print("File exists:")
print(report_path.exists())

print()
print("File extension:")
print(report_path.suffix)

print()
print("File size:")
print(report_path.stat().st_size, "bytes")


# ============================================================
# VALIDATION
# ============================================================

if not report_path.exists():

    raise RuntimeError(
        "PDF report was not created."
    )


if report_path.suffix.lower() != ".pdf":

    raise RuntimeError(
        "Generated report is not a PDF."
    )


if report_path.stat().st_size == 0:

    raise RuntimeError(
        "Generated PDF is empty."
    )


print()
print("PDF REPORT TEST PASSED")
print("=" * 45)