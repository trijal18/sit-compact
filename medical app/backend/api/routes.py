from flask import Blueprint, request, jsonify
from encryption import encrypt_data, decrypt_data
from models import db, MedicalRecord
from homomorphic import encrypt_data_homomorphic, decrypt_data_homomorphic
from differential_privacy import add_noise_to_data

api_routes = Blueprint('api', __name__)

# Upload medical record
@api_routes.route('/api/upload', methods=['POST'])
def upload_medical_record():
    data = request.form['data']
    encrypted_data = encrypt_data(data, b'YourEncryptionKey123')  # AES encryption key
    new_record = MedicalRecord(data=encrypted_data)
    db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Record uploaded successfully!"}), 200

# Get medical record
@api_routes.route('/api/get_record/<int:id>', methods=['GET'])
def get_medical_record(id):
    record = MedicalRecord.query.get(id)
    decrypted_data = decrypt_data(record.data, b'YourEncryptionKey123')
    return jsonify({"data": decrypted_data}), 200

# Example: Adding noise to data for differential privacy
@api_routes.route('/api/noisy_data', methods=['POST'])
def noisy_data():
    data = request.json.get('data')
    epsilon = request.json.get('epsilon', 1.0)
    noisy_data = add_noise_to_data(data, epsilon)
    return jsonify({"noisy_data": noisy_data}), 200
