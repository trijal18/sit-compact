from encryption.encryption import encrypt, decrypt 
# Function to encrypt the content of a file and save the result along with the key
def encrypt_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()   # Read the file content
        
        encrypted_text, key = encrypt(text)  # Encrypt the text
        
        # Write the encrypted text and key to the output file
        with open(output_file_path, 'w',encoding='utf-8') as file:
            file.write(f"Encrypted Text: {encrypted_text}\n")
            # file.write(f"Encryption Key: {key}\n")
        
        return key
        # print(f"File encrypted successfully. Encrypted text and key written to {output_file_path}")
    except Exception as e:
        print(f"Error: {e}")

# Function to decrypt the encrypted text in a file and save the result
def decrypt_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()  # Read the file content
            
            # Extract encrypted text and key from the file
            encrypted_text = lines[0].replace("Encrypted Text: ", "").strip()
            key = lines[1].replace("Encryption Key: ", "").strip()
        
        # Decrypt the text using the key
        decrypted_text = decrypt(encrypted_text, key)
        
        # Write the decrypted text to the output file
        with open(output_file_path, 'w') as file:
            file.write(f"Decrypted Text: {decrypted_text}\n")
        
        print(f"File decrypted successfully. Decrypted text written to {output_file_path}")
    except Exception as e:
        print(f"Error: {e}")
