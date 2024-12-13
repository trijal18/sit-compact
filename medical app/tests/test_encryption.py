import unittest
from encryption import encrypt_data, decrypt_data
from Crypto.Random import get_random_bytes

class TestEncryption(unittest.TestCase):
    
    def setUp(self):
        self.key = get_random_bytes(16)  # AES requires a 16-byte key

    def test_encryption_decryption(self):
        data = "Sensitive medical data"
        encrypted_data = encrypt_data(data, self.key)
        decrypted_data = decrypt_data(encrypted_data, self.key)
        self.assertEqual(decrypted_data, data)
    
    def test_invalid_key(self):
        data = "Sensitive medical data"
        encrypted_data = encrypt_data(data, self.key)
        invalid_key = get_random_bytes(16)
        with self.assertRaises(ValueError):
            decrypt_data(encrypted_data, invalid_key)

if __name__ == '__main__':
    unittest.main()
