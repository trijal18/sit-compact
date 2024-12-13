import random
import string

# # Function to generate a random key for encryption
# def generate_key(length):
#     return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# # Function to encrypt the input string
# def encrypt(text):
#     key = generate_key(len(text))  # Generate a random key of the same length as the text
#     encrypted_text = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, key))  # XOR encryption
#     return encrypted_text, key

# # Function to decrypt the encrypted text using the key
# def decrypt(encrypted_text, key):
#     decrypted_text = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(encrypted_text, key))  # XOR decryption
#     return decrypted_text

# Function to generate a random key of a given length
def generate_key(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to encrypt text using XOR encryption
def encrypt(text):
    key = generate_key(len(text))  # Generate a random key of the same length as the text
    encrypted_text = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, key))  # XOR encryption
    return encrypted_text, key

# Function to decrypt the encrypted text using the key
def decrypt(encrypted_text, key):
    decrypted_text = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(encrypted_text, key))  # XOR decryption
    return decrypted_text

# Example usage
if __name__ == "__main__":
    # Take input text from the user
    input_text = input("Enter text to encrypt: ")

    # Encrypt the text
    encrypted_text, encryption_key = encrypt(input_text)
    print(f"Encrypted Text: {encrypted_text}")
    print(f"Encryption Key: {encryption_key}")

    # Decrypt the text
    decrypted_text = decrypt(encrypted_text, encryption_key)
    print(f"Decrypted Text: {decrypted_text}")
