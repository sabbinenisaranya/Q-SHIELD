from pathlib import Path

from pipeline import QShieldPipeline

from crypto.public_key_loader import load_public_key


print("\n========================================")
print("   Q-SHIELD EXTERNAL PIPELINE TEST")
print("========================================")


# --------------------------------------------------
# Sample files
# --------------------------------------------------

sample_folder = Path(
    "Q_SHIELD_Sample_Uploads"
)

document_path = (
    sample_folder
    / "sample_01_business_authorization.pdf"
)

public_key_path = (
    sample_folder
    / "sample_01_business_authorization_public_key.pem"
)

signature_path = (
    sample_folder
    / "sample_01_business_authorization_signature.sig"
)


# --------------------------------------------------
# Check files
# --------------------------------------------------

if not document_path.exists():
    raise FileNotFoundError(
        f"Document not found: {document_path}"
    )

if not public_key_path.exists():
    raise FileNotFoundError(
        f"Public key not found: {public_key_path}"
    )

if not signature_path.exists():
    raise FileNotFoundError(
        f"Signature not found: {signature_path}"
    )


# --------------------------------------------------
# Read files
# --------------------------------------------------

document = document_path.read_bytes()

public_key_bytes = (
    public_key_path.read_bytes()
)

signature = signature_path.read_bytes()


# --------------------------------------------------
# Load public key
# --------------------------------------------------

public_key = load_public_key(
    public_key_bytes
)


# --------------------------------------------------
# Create pipeline
# --------------------------------------------------

pipeline = QShieldPipeline()

pipeline.train_anomaly_detector()


# --------------------------------------------------
# Analyze external signature
# --------------------------------------------------

result = (
    pipeline.analyze_external_signature(
        document=document,
        signature=signature,
        public_key=public_key
    )
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nDocument Hash:")
print(
    result["document_hash"]
)

print("\nSignature Valid:")
print(
    result["signature_valid"]
)

print("\nML Classification:")
print(
    result["ml_classification"]
)

print("\nAnomaly Score:")
print(
    result["anomaly_score"]
)

print("\nQuantum-Inspired Score:")
print(
    result["quantum_score"]
)

print("\nThreat Score:")
print(
    result["threat_score"]
)

print("\nRisk Level:")
print(
    result["risk_level"]
)

print("\nThreat Type:")
print(
    result["threat_type"]
)


print("\n========================================")
print("       TEST COMPLETE")
print("========================================")