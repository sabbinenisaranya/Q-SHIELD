from crypto.key_manager import generate_key_pair
from crypto.signer import sign_document
from crypto.verifier import verify_signature


print("\n========================================")
print("       Q-SHIELD DIGITAL SIGNATURE")
print("              TEST")
print("========================================")


# STEP 1: Generate keys
private_key, public_key = generate_key_pair()

print("\n[1] Key pair generated successfully")


# STEP 2: Create a document
document = b"Q-Shield secure digital document"

print("[2] Document created")


# STEP 3: Sign the document
document_hash, signature = sign_document(
    document,
    private_key
)

print("[3] Digital signature generated")

print("\nSHA-256 HASH:")
print(document_hash)


# STEP 4: Verify the original document
result = verify_signature(
    document,
    signature,
    public_key
)

print("\n[4] ORIGINAL DOCUMENT")

if result:
    print("    SIGNATURE: VALID")
else:
    print("    SIGNATURE: INVALID")


# STEP 5: Modify the document
modified_document = b"Q-Shield modified document"


# STEP 6: Verify the modified document
modified_result = verify_signature(
    modified_document,
    signature,
    public_key
)

print("\n[5] MODIFIED DOCUMENT")

if modified_result:
    print("    SIGNATURE: VALID")
else:
    print("    SIGNATURE: INVALID")


print("\n========================================")
print("              TEST COMPLETE")
print("========================================")