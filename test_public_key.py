from crypto.key_manager import generate_key_pair
from cryptography.hazmat.primitives import serialization

from crypto.public_key_loader import load_public_key


print("\n================================")
print(" PUBLIC KEY LOADING TEST")
print("================================")


private_key, public_key = generate_key_pair()


public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


print("\nGenerated public key:")

print(
    public_key_pem.decode()
)


loaded_key = load_public_key(
    public_key_pem
)


print("\nPublic key loaded successfully.")

print(
    "Key type:",
    type(loaded_key).__name__
)


print("\n================================")
print(" TEST COMPLETE")
print("================================")