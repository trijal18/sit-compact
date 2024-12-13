from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

# Configure MongoDB connection
client = MongoClient("mongodb+srv://trijalvshinde:zh3Lc25IyxEdqVqo@sit-cluster.fns1g.mongodb.net/") 
# mongo = PyMongo(app)

db = client['sit-compact'] 
  
# Create collection named data if it doesn't exist already 
doctor_collection = db['doctors']
patient_collection = db['patients']

#for doctor login
@app.route('/add_doctor',methods=['GET'])
def doctor_login():
    return render_template("doctor_login.html")

# POST Endpoint: Add a new doctor
@app.route('/doctor', methods=['POST'])
def add_doctor():
    try:
        if request.is_json:
            data = request.json  # Handle JSON request
        else:
            # Handle form submission (application/x-www-form-urlencoded)
            data = request.form.to_dict()

        # Validate required fields
        if not data.get('name') or not data.get('speciality'):
            return jsonify({"error": "Name and Speciality are required"}), 400

        # Insert new doctor into the database
        doctor_id = doctor_collection.insert_one({
            "name": data['name'],
            "speciality": data['speciality'],
            "patients": data.get('patients', "").split(',') if data.get('patients') else []  # Split patients by commas
        }).inserted_id

        # Respond with success
        return jsonify({"message": "Doctor added", "id": str(doctor_id)}), 201

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

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
@app.route('/add_patient',methods=['GET'])
def patient_login():
    return render_template("patient_login.html")

@app.route('/patient', methods=['POST'])
def add_patient():
    try:
        if request.is_json:
            data = request.json  # Handle JSON request
        else:
            # Handle form submission (application/x-www-form-urlencoded)
            data = request.form.to_dict()

        # Validate required fields
        if not data.get('name'):
            return jsonify({"error": "Name is required"}), 400

        # Insert new patient into the database
        patient_id = patient_collection.insert_one({
            "name": data['name'],
            "doctors": data.get('doctors', "").split(',') if data.get('doctors') else []  # Split doctors by commas
        }).inserted_id

        # Respond with success
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
