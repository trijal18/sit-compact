import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from typing import Dict, Union

class SimpleKeyEncryption:
    def _init_(self, key_size: int = 2048):
        """
        Initialize encryption system
        
        :param key_size: RSA key size in bits
        """
        self.key_size = key_size
    
    def generate_key_pair(self) -> tuple:
        """
        Generate RSA key pair
        
        :return: Tuple of (private_key, public_key)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def encrypt(self, data: Union[str, bytes], public_key) -> Dict[str, str]:
        """
        Encrypt data:
        1. Generate AES symmetric key
        2. Encrypt data with AES
        3. Encrypt AES key with public key
        
        :param data: Data to encrypt
        :param public_key: Receiver's public key
        :return: Encrypted payload dictionary
        """
        # Ensure data is in bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Generate AES symmetric key (32 bytes = 256 bits)
        symmetric_key = os.urandom(32)
        
        # Generate IV for AES (16 bytes)
        iv = os.urandom(16)
        
        # AES encryption of data
        cipher = Cipher(
            algorithms.AES(symmetric_key), 
            modes.CFB(iv), 
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        
        # Encrypt AES symmetric key with public key
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Return base64 encoded components
        return {
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'encrypted_symmetric_key': base64.b64encode(encrypted_symmetric_key).decode('utf-8')
        }
    
    def decrypt(self, encrypted_payload: Dict[str, str], private_key) -> bytes:
        """
        Decrypt data:
        1. Decrypt AES key with private key
        2. Use AES key to decrypt data
        
        :param encrypted_payload: Encryption result dictionary
        :param private_key: Receiver's private key
        :return: Decrypted data
        """
        # Decode base64 encoded components
        encrypted_data = base64.b64decode(encrypted_payload['encrypted_data'])
        iv = base64.b64decode(encrypted_payload['iv'])
        encrypted_symmetric_key = base64.b64decode(encrypted_payload['encrypted_symmetric_key'])
        
        # Decrypt AES symmetric key using private key
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # AES decryption
        cipher = Cipher(
            algorithms.AES(symmetric_key), 
            modes.CFB(iv), 
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Return decrypted data
        return decryptor.update(encrypted_data) + decryptor.finalize()

def main():
    # Create encryption system
    encryption = SimpleKeyEncryption()
    
    # Generate key pair for receiver
    receiver_private_key, receiver_public_key = encryption.generate_key_pair()
    
    # Message to encrypt
    message = "Secure communication using AES and public key encryption!"
    
    # Encrypt message
    encrypted_payload = encryption.encrypt(message, receiver_public_key)
    print("Encrypted Payload:")
    for key, value in encrypted_payload.items():
        print(f"{key}: {value}")
    
    # Decrypt message
    decrypted_message = encryption.decrypt(encrypted_payload, receiver_private_key)
    
    # Verify decryption
    print("\nDecrypted Message:", decrypted_message.decode('utf-8'))
    assert message == decrypted_message.decode('utf-8'), "Decryption failed!"

if __name__ == "__main__":
    main()