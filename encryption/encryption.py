from cryptography.fernet import Fernet

def generate_key():
    """
    Generate a new encryption key.
    Save this key securely as it will be required for decryption.
    """
    return Fernet.generate_key()

def encrypt(data: str, key: bytes) -> bytes:
    """
    Encrypts the provided data using the given key.
    
    :param data: The plaintext data to encrypt (string).
    :param key: The encryption key (bytes).
    :return: Encrypted data (bytes).
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt(encrypted_data: bytes, key: bytes) -> str:
    """
    Decrypts the provided encrypted data using the given key.
    
    :param encrypted_data: The encrypted data to decrypt (bytes).
    :param key: The decryption key (bytes).
    :return: Decrypted plaintext data (string).
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# Example Usage
if __name__ == "__main__":
    # Generate a key and print it (save this key securely!)
    key = generate_key()
    print("Encryption Key:", key)

    # Data to encrypt
    original_data = "Sensitive data to encrypt"
    print("Original Data:", original_data)

    # Encrypt the data
    encrypted = encrypt(original_data, key)
    print("Encrypted Data:", encrypted)

    # Decrypt the data
    decrypted = decrypt(encrypted, key)
    print("Decrypted Data:", decrypted)