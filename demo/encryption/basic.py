from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# Function to generate a symmetric key
def generate_key():
    return os.urandom(32)  # Generates a 256-bit random key

# Function to encrypt a message
def encrypt_message(key, plaintext):
    # Create a random 16-byte IV (Initialization Vector)
    iv = os.urandom(16)
    
    # Create AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the plaintext to a multiple of the block size (16 bytes for AES)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
    
    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return both the IV and the ciphertext (IV is needed for decryption)
    return iv + ciphertext

# Function to decrypt a message
def decrypt_message(key, ciphertext):
    # Split the IV and the actual ciphertext
    iv = ciphertext[:16]  # The first 16 bytes are the IV
    actual_ciphertext = ciphertext[16:]
    
    # Create AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    
    # Remove the padding from the plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    return plaintext.decode('utf-8')

# Example Usage
if __name__ == "__main__":
    # Step 1: Generate a symmetric key
    key = generate_key()
    print("Symmetric Key:", key.hex())
    
    # Step 2: Encrypt a message
    message = "This is a secret message"
    print("Original Message:", message)
    encrypted_message = encrypt_message(key, message)
    print("Encrypted Message:", encrypted_message.hex())
    
    # Step 3: Decrypt the message
    decrypted_message = decrypt_message(key, encrypted_message)
    print("Decrypted Message:", decrypted_message)
