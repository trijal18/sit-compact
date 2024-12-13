from flask import Flask, request, jsonify, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure MongoDB connection
client = MongoClient("mongodb+srv://trijalvshinde:zh3Lc25IyxEdqVqo@sit-cluster.fns1g.mongodb.net/")
# mongo = PyMongo(app)

db = client['sit-compact']

# Create collection named data if it doesn't exist already
doctor_collection = db['doctors']
patient_collection = db['patients']

# For doctor signup
@app.route('/doctor_signup', methods=['GET'])
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
                return redirect(f"{doctor['_id']}")  # Corrected f-string
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

# For patient signup
@app.route('/patient_signup', methods=['GET'])
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

        return jsonify({"message": "Patient added", "id": str(patient_id)}), 201

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

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
                return redirect(f"{patient['_id']}")  # Corrected f-string
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

if __name__ == "__main__":
    app.run(debug=True)
