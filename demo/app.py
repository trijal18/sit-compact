from flask import Flask, request, jsonify, render_template, redirect, make_response, send_file
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.security import generate_password_hash,check_password_hash
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError
import random, string
import os
# from encryption.xor import encrypt,decrypt
# from encryption.en import decrypt_message, encrypt_message
from encryption.basic import decrypt_message, encrypt_message

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Directory to temporarily save files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initialize Azure Blob service client using your connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=shareencrypt;AccountKey=KvutLtrtXl0b6nuC+W29ABje2ZpHm7yyMBKcdcCIOOIbs2u0rkzSb61vRtJ07qeK8GCJBf7/9qRh+AStGam16Q==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Define the container name
CONTAINER_NAME = "store"

app = Flask(__name__)

# Configure MongoDB connection
client = MongoClient("mongodb+srv://trijalvshinde:zh3Lc25IyxEdqVqo@sit-cluster.fns1g.mongodb.net/") 
# mongo = PyMongo(app)

db = client['sit-compact'] 
  
# Create collection named data if it doesn't exist already 
doctor_collection = db['doctors']
patient_collection = db['patients']
key_collection=db['keys']
public_keys_collection=db['public_keys']

KEY="cbf9b6e70a193159411bade2cbfc4d74fc155cdec26c706dfd637da875bc4236"

@app.route('/',methods=['GET'])
def home():
    return render_template("index.html")

#for doctor login
@app.route('/doctor_signup',methods=['GET'])
def doctor_signup():
    return render_template("doctor_signup.html")

# POST Endpoint: Add a new doctor
@app.route('/doctor', methods=['POST'])
def add_doctor():
    name = request.form.get('name')
    speciality = request.form.get('speciality')
    password = request.form.get('password')
    patients = request.form.get('patients', '').split(',')

    if not name or not speciality or not password:
        return jsonify({"error": "Name, Speciality, and Password are required"}), 400

    hashed_password = generate_password_hash(password, method='scrypt')

    doctor_id = doctor_collection.insert_one({
        "name": name,
        "speciality": speciality,
        "password": hashed_password,
        "patients": patients
    }).inserted_id

    return jsonify({"message": "Doctor added", "id": str(doctor_id)}), 201

# @app.route('/doctor', methods=['POST'])
# def add_doctor():
#     data = request.json
#     if not data.get('name') or not data.get('speciality'):
#         return jsonify({"error": "Name and Speciality are required"}), 400

#     doctor_id = doctor_collection.insert_one({
#         "name": data['name'],
#         "speciality": data['speciality'],
#         "patients": data.get('patients', [])  # Default to empty array
#     }).inserted_id

# return jsonify({"message": "Doctor added", "id": str(doctor_id)}), 201

@app.route('/doctor/login', methods=['GET', 'POST'])
def login_doctor():
    if request.method == 'GET':
        return render_template("doctor_login.html")
    
    if request.method == 'POST':
        try:
            # Handle form submission (application/x-www-form-urlencoded)
            data = request.form.to_dict()

            # Validate required fields
            if not data.get('name') or not data.get('password'):
                return jsonify({"error": "Name and Password are required"}), 400

            # Find the doctor by name
            doctor = doctor_collection.find_one({"name": data['name']})

            if not doctor:
                return jsonify({"error": "Doctor not found"}), 404

            # Check if the provided password matches the stored hashed password
            if check_password_hash(doctor['password'], data['password']):
                return redirect(f'{doctor['_id']}')
                # return jsonify({"message": "Login successful", "doctor_id": str(doctor['_id'])}), 200
            else:
                return jsonify({"error": "Invalid password"}), 401

        except Exception as e:
            # Handle unexpected errors
            return jsonify({"error": "An error occurred", "details": str(e)}), 500


# GET Endpoint: Get all doctors
@app.route('/doctor_list', methods=['GET'])
def get_doctors():
    doctors = list(doctor_collection.find())
    for doctor in doctors:
        doctor["_id"] = str(doctor["_id"])  # Convert ObjectId to string
    return jsonify(doctors), 200

@app.route('/doctor/<doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    try:
        # Attempt to convert doctor_id to ObjectId
        doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})
        if not doctor:
            return render_template('doctor.html', error="Doctor not found"), 404

        # Convert ObjectId to string for rendering
        doctor["_id"] = str(doctor["_id"])
        return render_template('doctor.html', doctor=doctor)

    except InvalidId:
        # Handle invalid ObjectId format
        return render_template('doctor.html', error="Invalid doctor ID format"), 400

    except Exception as e:
        # Handle unexpected errors
        return render_template('doctor.html', error=f"An error occurred: {str(e)}"), 500


################################################################################################################################################################################################

#for patient login
@app.route('/patient_signup',methods=['GET'])
def patient_signup():
    return render_template("patient_signup.html")

@app.route('/patient', methods=['POST'])
def add_patient():
    try:
        # Handle form submission (application/x-www-form-urlencoded)
        data = request.form.to_dict()

        # Validate required fields
        if not data.get('name') or not data.get('password'):
            return jsonify({"error": "Name and Password are required"}), 400

        # Hash the password before saving (using sha256 as an example)
        hashed_password = generate_password_hash(data['password'], method='scrypt')

        # Insert new patient into the database
        patient_id = patient_collection.insert_one({
            "name": data['name'],
            "password": hashed_password,
            "doctors": data.get('doctors', "").split(',') if data.get('doctors') else []  # Split doctors by commas
        }).inserted_id

        # Respond with success
        # return redirect("patient/"+str(patient_id))
        return jsonify({"message": "Patient added", "id": str(patient_id)}), 201

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
    
# # POST Endpoint: Add a new patient
# @app.route('/patient', methods=['POST'])
# def add_patient():
#     data = request.json
#     if not data.get('name'):
#         return jsonify({"error": "Name is required"}), 400

#     patient_id = patient_collection.insert_one({
#         "name": data['name'],
#         "doctors": data.get('doctors', [])  # Default to empty array
#     }).inserted_id

#     return jsonify({"message": "Patient added", "id": str(patient_id)}), 201

# fotr patient login
@app.route('/patient/login', methods=['GET', 'POST'])
def login_patient():
    if request.method == 'GET':
        return render_template("patient_login.html")
    
    if request.method == 'POST':
        try:
            # Handle form submission (application/x-www-form-urlencoded)
            data = request.form.to_dict()

            # Validate required fields
            if not data.get('name') or not data.get('password'):
                return jsonify({"error": "Name and Password are required"}), 400

            # Find the patient by name
            patient = patient_collection.find_one({"name": data['name']})

            if not patient:
                return jsonify({"error": "Patient not found"}), 404

            # Check if the provided password matches the stored hashed password
            if check_password_hash(patient['password'], data['password']):
                return redirect(f'{patient['_id']}')
                # return jsonify({"message": "Login successful", "patient_id": str(patient['_id'])}), 200
            else:
                return jsonify({"error": "Invalid password"}), 401

        except Exception as e:
            # Handle unexpected errors
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/patient/<patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    try:
        # Attempt to convert patient_id to ObjectId
        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            return render_template('patient.html', error="Patient not found"), 404

        # Convert ObjectId to string
        patient["_id"] = str(patient["_id"])
        return render_template('patient.html', patient=patient)

    except InvalidId:
        # Handle invalid ObjectId format
        return render_template('patient.html', error="Invalid patient ID format"), 400

    except Exception as e:
        # Handle unexpected errors
        return render_template('patient.html', error=f"An error occurred: {str(e)}"), 500


# GET Endpoint: Get all patients
@app.route('/patient_list', methods=['GET'])
def get_patients():
    patients = list(patient_collection.find())
    for patient in patients:
        patient["_id"] = str(patient["_id"])  # Convert ObjectId to string
    return jsonify(patients), 200

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
        de=decrypt_message(KEY,file_content)

        return jsonify({'file_content': file_content,'de':de})

    except ResourceNotFoundError:
        return jsonify({'error': f'File {file_name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/upload')
def upload():
    return render_template('upload_file.html')
# Route to write a file to Azure Blob Storage
@app.route('/upload_file', methods=['POST'])
def upload_file(file_name=None,file_content=None):
    if file_name==None:
        file_content = request.form.get('file_content')
        file_name = request.form.get('file_name')

    # Check if file_name or file_content is missing
    # if not file_name or not file_content:
    #     return jsonify({'error': 'File name and content are required'}), 400   

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
        enc_content=encrypt_message(publiccontent)
        upload_file(new_file,enc_content)

        # Delete the file after processing
        os.remove(file_path)  
        # key_collection.insert_one({
        #     "public_key": key,
        #     "file_name": new_file,
        # }).inserted_id
    # Return the JSON response with status code 200
        return jsonify({"message": f"file_name={new_file}"})

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

