import random
import math

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Function to generate random prime numbers
def generate_prime():
    while True:
        num = random.randint(100, 1000)  # We choose a range for simplicity
        if is_prime(num):
            return num

# Function to calculate modular inverse
def mod_inverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None

# Key Generation for KEM
def generate_keys():
    p = generate_prime()
    q = generate_prime()

    n = p * q  # modulus for both public and private keys
    phi = (p - 1) * (q - 1)  # Euler's Totient

    e = 65537  # Common choice for e
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = mod_inverse(e, phi)

    public_key = (e, n)  # Public key (e, n)
    private_key = (d, n)  # Private key (d, n)

    return public_key, private_key

# KEM Encapsulation (Encapsulating a symmetric key)
def encapsulate(public_key):
    e, n = public_key

    # Generate a random symmetric key (for simplicity, we'll use a random 16-byte key)
    symmetric_key = random.getrandbits(128).to_bytes(16, byteorder='big')

    # Encapsulate the key (C = symmetric_key^e % n) - Simplified for illustration
    C = int.from_bytes(symmetric_key, byteorder='big')
    C = pow(C, e, n)
    
    return C, symmetric_key

# KEM Decapsulation (Decapsulating the symmetric key)
def decapsulate(private_key, C):
    d, n = private_key

    # Decapsulate the key (symmetric_key = C^d % n)
    symmetric_key_int = pow(C, d, n)
    symmetric_key = symmetric_key_int.to_bytes(16, byteorder='big')
    
    return symmetric_key

# Symmetric Encryption (XOR encryption)
def encrypt(message, symmetric_key):
    encrypted_message = bytearray()
    for i in range(len(message)):
        encrypted_message.append(message[i] ^ symmetric_key[i % len(symmetric_key)])
    return bytes(encrypted_message)

# Symmetric Decryption (XOR decryption)
def decrypt(encrypted_message, symmetric_key):
    decrypted_message = bytearray()
    for i in range(len(encrypted_message)):
        decrypted_message.append(encrypted_message[i] ^ symmetric_key[i % len(symmetric_key)])
    return bytes(decrypted_message)

# Example Usage
public_key, private_key = generate_keys()
print("Public Key:", public_key)
print("Private Key:", private_key)

# Sender encapsulates the symmetric key
C, symmetric_key = encapsulate(public_key)
print("Encapsulated Key (C):", C)

# Receiver decapsulates the symmetric key
decapsulated_key = decapsulate(private_key, C)
print("Decapsulated Symmetric Key:", decapsulated_key)

# Verify that the decapsulated key matches the original symmetric key
if symmetric_key != decapsulated_key:
    print("Decapsulation failed: Keys do not match")
else:
    print("Decapsulation successful: Keys match")

# Encrypt a message using the symmetric key
message = b"Hello, this is a secret message."
print("Original Message:", message)

encrypted_message = encrypt(message, symmetric_key)
print("Encrypted Message:", encrypted_message)

# Decrypt the message using the symmetric key
decrypted_message = decrypt(encrypted_message, symmetric_key)
print("Decrypted Message:", decrypted_message)

# Verify that the decrypted message matches the original message
if message != decrypted_message:
    print("Decryption failed: Messages do not match")
else:
    print("Decryption successful: Messages match")
