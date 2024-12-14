from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Step 1: Generate RSA Key Pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Step 2: Encrypt Message
def encrypt_message(public_key, message):
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# Step 3: Decrypt Message
def decrypt_message(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

# Example Usage
if __name__ == "__main__":
    # Generate keys
    private_key, public_key = generate_key_pair()

    # Serialize keys for demonstration (optional)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    print("Private Key:")
    print(private_pem.decode())
    print("Public Key:")
    print(public_pem.decode())

    # Encrypt a message
    message = "Hello, this is a secret!"
    print("\nOriginal Message:", message)
    ciphertext = encrypt_message(public_key, message)
    print("\nEncrypted Message:", ciphertext)

    # Decrypt the message
    decrypted_message = decrypt_message(private_key, ciphertext)
    print("\nDecrypted Message:", decrypted_message)
