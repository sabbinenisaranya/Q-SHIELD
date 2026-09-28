from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def verify_signature(document: bytes, signature: bytes, public_key):
    """
    Verify a digital signature.

    Returns:
        True  = signature is valid
        False = signature is invalid
    """

    try:

        public_key.verify(
            signature,
            document,
            ec.ECDSA(hashes.SHA256())
        )

        return True

    except InvalidSignature:

        return False