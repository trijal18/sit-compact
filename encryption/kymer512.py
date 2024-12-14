from pqc_kyber import Kyber512
import os

def kem_keygen():
    """
    Generate key pair for KEM
    :return: (public_key, secret_key)
    """
    kyber = Kyber512()
    public_key, secret_key = kyber.keygen()
    return public_key, secret_key

def kem_encapsulate(public_key):
    """
    Encapsulate a symmetric key using the public key.
    :param public_key: Kyber public key
    :return: (ciphertext, shared_secret)
    """
    kyber = Kyber512()
    ciphertext, shared_secret = kyber.encapsulate(public_key)
    return ciphertext, shared_secret

def kem_decapsulate(secret_key, ciphertext):
    """
    Decapsulate the ciphertext using the secret key.
    :param secret_key: Kyber secret key
    :param ciphertext: Ciphertext to decapsulate
    :return: shared_secret
    """
    kyber = Kyber512()
    shared_secret = kyber.decapsulate(secret_key, ciphertext)
    return shared_secret

# Example usage
public_key, secret_key = kem_keygen()
print(f"Public Key: {public_key}")
print(f"Secret Key: {secret_key}")

# Encapsulation
ciphertext, encapsulated_shared_secret = kem_encapsulate(public_key)
print(f"Ciphertext: {ciphertext}")
print(f"Encapsulated Shared Secret: {encapsulated_shared_secret}")

# Decapsulation
decapsulated_shared_secret = kem_decapsulate(secret_key, ciphertext)
print(f"Decapsulated Shared Secret: {decapsulated_shared_secret}")

# Check if both shared secrets are the same
assert encapsulated_shared_secret == decapsulated_shared_secret, "Shared secrets do not match!"
print("Shared secrets match.")
