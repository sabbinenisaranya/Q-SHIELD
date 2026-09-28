import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def hash_document(document: bytes) -> str:
    """
    Create a SHA-256 hash of the document.
    """

    return hashlib.sha256(document).hexdigest()


def sign_document(document: bytes, private_key):
    """
    Create a digital signature for the document.
    """

    signature = private_key.sign(
        document,
        ec.ECDSA(hashes.SHA256())
    )

    document_hash = hash_document(document)

    return document_hash, signature