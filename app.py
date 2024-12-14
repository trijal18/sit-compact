import jwt
import datetime
from flask import Flask, request, jsonify, render_template, redirect, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB and JWT secret from environment variables
MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

# Set up MongoDB
client = MongoClient(MONGO_URI)
db = client['sit-compact']
doctor_collection = db['doctors']
patient_collection = db['patients']

# Route to login doctor and generate token
@app.route('/doctor/login', methods=['POST'])
def login_doctor():
    data = request.form.to_dict()

    if not data.get('name') or not data.get('password'):
        return jsonify({"error": "Name and Password are required"}), 400

    doctor = doctor_collection.find_one({"name": data['name']})

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    if check_password_hash(doctor['password'], data['password']):
        # Create JWT token
        token = jwt.encode({
            'doctor_id': str(doctor['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration
        }, JWT_SECRET, algorithm='HS256')

        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401

# Route to login patient and generate token
@app.route('/patient/login', methods=['POST'])
def login_patient():
    data = request.form.to_dict()
<<<<<<< HEAD

    if not data.get('name') or not data.get('password'):
        return jsonify({"error": "Name and Password are required"}), 400

    patient = patient_collection.find_one({"name": data['name']})

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    if check_password_hash(patient['password'], data['password']):
        # Create JWT token
        token = jwt.encode({
            'patient_id': str(patient['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration
        }, JWT_SECRET, algorithm='HS256')

        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401

# Route to protect with token-based auth (for doctors)
@app.route('/doctor/dashboard', methods=['GET'])
def doctor_dashboard():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        # Remove 'Bearer ' prefix from the token
        token = token.split(" ")[1]
        
        # Decode the token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        doctor_id = decoded['doctor_id']

        # Fetch doctor details
        doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})

        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        return jsonify({"doctor": doctor["name"], "speciality": doctor["speciality"]}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

# Route to protect with token-based auth (for patients)
@app.route('/patient/dashboard', methods=['GET'])
def patient_dashboard():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        # Remove 'Bearer ' prefix from the token
        token = token.split(" ")[1]

        # Decode the token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        patient_id = decoded['patient_id']

        # Fetch patient details
        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})

        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        return jsonify({"patient": patient["name"]}), 200
=======

    if not data.get('name') or not data.get('password'):
        return jsonify({"error": "Name and Password are required"}), 400

    patient = patient_collection.find_one({"name": data['name']})

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    if check_password_hash(patient['password'], data['password']):
        # Create JWT token
        token = jwt.encode({
            'patient_id': str(patient['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration
        }, JWT_SECRET, algorithm='HS256')

        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401

# Route to protect with token-based auth (for doctors)
@app.route('/doctor/dashboard', methods=['GET'])
def doctor_dashboard():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        # Remove 'Bearer ' prefix from the token
        token = token.split(" ")[1]
        
        # Decode the token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        doctor_id = decoded['doctor_id']

        # Fetch doctor details
        doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})

        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        return jsonify({"doctor": doctor["name"], "speciality": doctor["speciality"]}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

# Route to protect with token-based auth (for patients)
@app.route('/patient/dashboard', methods=['GET'])
def patient_dashboard():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        # Remove 'Bearer ' prefix from the token
        token = token.split(" ")[1]

        # Decode the token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        patient_id = decoded['patient_id']

        # Fetch patient details
        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})

        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        return jsonify({"patient": patient["name"]}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
        
################################################################################################################################################################################################


@app.route('/download')
def download():
    return render_template('download_file.html')
# Route to read a file from Azure Blob Storage
@app.route('/download_file', methods=['GET'])
def download_file():
    file_name = request.args.get('file_name')

    if not file_name:
        return jsonify({'error': 'No file name provided'}), 400

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)
        
        # Download the blob data
        blob_data = blob_client.download_blob()
        file_content = blob_data.readall().decode('utf-8')

        return jsonify({'file_content': file_content})

    except ResourceNotFoundError:
        return jsonify({'error': f'File {file_name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/upload')
def upload():
    return render_template('upload_file.html')
# Route to write a file to Azure Blob Storage
@app.route('/upload_file', methods=['POST'])
def upload_file(file_name,file_content):
    file_content = request.form.get('file_content')
    file_name = request.form.get('file_name')

    # Check if file_name or file_content is missing
    if not file_name or not file_content:
        return jsonify({'error': 'File name and content are required'}), 400   

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        # Upload the blob data (file content)
        blob_client.upload_blob(file_content, overwrite=True)

        # Return success response with 200 OK and structured JSON
        return jsonify({'message': f'File {file_name} uploaded successfully'}), 200

    except Exception as e:
        # Handle exceptions and return error message with 500 status code
        return jsonify({'error': str(e)}), 500

@app.route('/data_encrypt')
def data_encrypt():
    return render_template('upload_data.html')
# Endpoint to upload and process a text file
@app.route('/upload_data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '' or not file.filename.endswith('.txt'):
        return jsonify({"error": "Please upload a valid .txt file"}), 400

    try:
        # Save the file temporarily
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Use 'with open' to read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        random_string = lambda n=10: ''.join(random.choices(string.ascii_letters + string.digits, k=n))
        new_file = random_string() + ".txt"
        # Pass the content to the processing function
        enc_content,key=encrypt(content)
        upload_file(new_file,enc_content)

        # Delete the file after processing
        os.remove(file_path)  
        key_collection.insert_one({
            "public_key": key,
            "file_name": new_file,
        }).inserted_id
    # Return the JSON response with status code 200
        return jsonify({"message": f"key: {key} \n file_name={new_file}"})

    except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/decrypt_data', methods=['GET'])
def decrypt_data():
    # Renders the HTML form where the user will input file name and key
    return render_template('download_data.html')

@app.route('/download_data', methods=['POST'])
def download_decrypted_data():
    file_name = request.form.get('file_name')
    key = request.form.get('key').encode('utf-8')  # Ensure the key is in bytes

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        # Download the encrypted blob data
        blob_data = blob_client.download_blob()
        cipher_text = blob_data.readall()

        text=decrypt(cipher_text,key)
        with open("decrypted_file_content.txt", "w") as f:
            f.write(text)

        # Return the decrypted file as a downloadable response
        return send_file("decrypted_file_content.txt", as_attachment=True, download_name=file_name)

    except ResourceNotFoundError:
        return jsonify({'error': f'File {file_name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 8d409d163b52a4537a962df058e7396e470c8d61

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
        
################################################################################################################################################################################################


@app.route('/download')
def download():
    return render_template('download_file.html')
# Route to read a file from Azure Blob Storage
@app.route('/download_file', methods=['GET'])
def download_file():
    file_name = request.args.get('file_name')

    if not file_name:
        return jsonify({'error': 'No file name provided'}), 400

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)
        
        # Download the blob data
        blob_data = blob_client.download_blob()
        file_content = blob_data.readall().decode('utf-8')

        return jsonify({'file_content': file_content})

    except ResourceNotFoundError:
        return jsonify({'error': f'File {file_name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/upload')
def upload():
    return render_template('upload_file.html')
# Route to write a file to Azure Blob Storage
@app.route('/upload_file', methods=['POST'])
def upload_file(file_name,file_content):
    file_content = request.form.get('file_content')
    file_name = request.form.get('file_name')

    # Check if file_name or file_content is missing
    if not file_name or not file_content:
        return jsonify({'error': 'File name and content are required'}), 400   

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        # Upload the blob data (file content)
        blob_client.upload_blob(file_content, overwrite=True)

        # Return success response with 200 OK and structured JSON
        return jsonify({'message': f'File {file_name} uploaded successfully'}), 200

    except Exception as e:
        # Handle exceptions and return error message with 500 status code
        return jsonify({'error': str(e)}), 500

@app.route('/data_encrypt')
def data_encrypt():
    return render_template('upload_data.html')
# Endpoint to upload and process a text file
@app.route('/upload_data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '' or not file.filename.endswith('.txt'):
        return jsonify({"error": "Please upload a valid .txt file"}), 400

    try:
        # Save the file temporarily
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Use 'with open' to read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        random_string = lambda n=10: ''.join(random.choices(string.ascii_letters + string.digits, k=n))
        new_file = random_string() + ".txt"
        # Pass the content to the processing function
        enc_content,key=encrypt(content)
        upload_file(new_file,enc_content)

        # Delete the file after processing
        os.remove(file_path)  
        key_collection.insert_one({
            "public_key": key,
            "file_name": new_file,
        }).inserted_id
    # Return the JSON response with status code 200
        return jsonify({"message": f"key: {key} \n file_name={new_file}"})

    except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/decrypt_data', methods=['GET'])
def decrypt_data():
    # Renders the HTML form where the user will input file name and key
    return render_template('download_data.html')

@app.route('/download_data', methods=['POST'])
def download_decrypted_data():
    file_name = request.form.get('file_name')
    key = request.form.get('key').encode('utf-8')  # Ensure the key is in bytes

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        # Download the encrypted blob data
        blob_data = blob_client.download_blob()
        cipher_text = blob_data.readall()

        text=decrypt(cipher_text,key)
        with open("decrypted_file_content.txt", "w") as f:
            f.write(text)

        # Return the decrypted file as a downloadable response
        return send_file("decrypted_file_content.txt", as_attachment=True, download_name=file_name)

    except ResourceNotFoundError:
        return jsonify({'error': f'File {file_name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
