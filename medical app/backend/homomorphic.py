import tenseal as ts

# Initialize a context for homomorphic encryption
def initialize_homomorphic_context():
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 60])
    context.generate_galois_keys()
    return context

# Encrypt data
def encrypt_data_homomorphic(context, data):
    encrypted_data = context.encrypt([data])
    return encrypted_data

# Decrypt data
def decrypt_data_homomorphic(context, encrypted_data):
    decrypted_data = context.decrypt(encrypted_data)
    return decrypted_data[0]

# Homomorphic addition (example operation)
def add_homomorphic(context, encrypted_data1, encrypted_data2):
    return encrypted_data1 + encrypted_data2
