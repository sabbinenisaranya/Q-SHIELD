from cryptography.hazmat.primitives import serialization


def load_public_key(public_key_bytes):
    """
    Load a PEM encoded public key.
    """

    public_key = serialization.load_pem_public_key(
        public_key_bytes
    )

    return public_key