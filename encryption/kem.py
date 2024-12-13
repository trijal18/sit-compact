from pqcrypto.kem.kyber512 import generate_keypair, encapsulate, decapsulate

def generate_keys():
    """Generates public and private keys for Kyber512 KEM."""
    public_key, private_key = generate_keypair()
    return public_key, private_key

def encapsulate_key(public_key):
    """Encapsulates a shared secret using the receiver's public key.

    Args:
        public_key (bytes): The receiver's public key.

    Returns:
        tuple: A ciphertext and a shared secret.
    """
    ciphertext, shared_secret = encapsulate(public_key)
    return ciphertext, shared_secret

def decapsulate_key(ciphertext, private_key):
    """Decapsulates the ciphertext using the receiver's private key to derive the shared secret.

    Args:
        ciphertext (bytes): The ciphertext received from the sender.
        private_key (bytes): The receiver's private key.

    Returns:
        bytes: The shared secret.
    """
    shared_secret = decapsulate(ciphertext, private_key)
    return shared_secret

# Example usage
def main():
    # Step 1: Key Generation (Receiver)
    public_key, private_key = generate_keys()
    print("Public Key:", public_key.hex())
    print("Private Key:", private_key.hex())

    # Step 2: Encapsulation (Sender)
    ciphertext, shared_secret_sender = encapsulate_key(public_key)
    print("Ciphertext (ct):", ciphertext.hex())
    print("Shared Secret (Sender):", shared_secret_sender.hex())

    # Step 3: Decapsulation (Receiver)
    shared_secret_receiver = decapsulate_key(ciphertext, private_key)
    print("Shared Secret (Receiver):", shared_secret_receiver.hex())

    # Verify both shared secrets are identical
    assert shared_secret_sender == shared_secret_receiver, "Shared secrets do not match!"
    print("Key exchange successful! Shared secret established.")

if _name_ == "_main_":
    main()