from cryptography.hazmat.primitives import serialization

from crypto.key_manager import generate_key_pair
from crypto.signer import sign_document
from crypto.verifier import verify_signature
from crypto.public_key_loader import load_public_key


print("\n================================")
print(" EXTERNAL SIGNATURE TEST")
print("================================")


# --------------------------------------------------
# 1. Generate a key pair
# --------------------------------------------------

private_key, public_key = generate_key_pair()

print("\n1. Key pair generated.")


# --------------------------------------------------
# 2. Create a document
# --------------------------------------------------

document = (
    b"This is a Q-SHIELD external signature test."
)

print("2. Test document created.")


# --------------------------------------------------
# 3. Sign the document
# --------------------------------------------------

document_hash, signature = sign_document(
    document,
    private_key
)

print("3. Digital signature created.")


# --------------------------------------------------
# 4. Convert public key to PEM format
# --------------------------------------------------

public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("4. Public key exported to PEM.")


# --------------------------------------------------
# 5. Load the public key again
# --------------------------------------------------

loaded_public_key = load_public_key(
    public_key_pem
)

print("5. Public key loaded successfully.")


# --------------------------------------------------
# 6. Verify the signature
# --------------------------------------------------

is_valid = verify_signature(
    document,
    signature,
    loaded_public_key
)


print("\n================================")

if is_valid:
    print(" SIGNATURE VALID")
else:
    print(" SIGNATURE INVALID")

print("================================")


# --------------------------------------------------
# 7. Test modified document
# --------------------------------------------------

modified_document = (
    b"This document has been modified."
)

modified_valid = verify_signature(
    modified_document,
    signature,
    loaded_public_key
)


print("\nModified document verification:")

if modified_valid:
    print("ERROR: Modified document was accepted.")
else:
    print("CORRECT: Modified document rejected.")


print("\n================================")
print(" TEST COMPLETE")
print("================================")