from flask import Flask, request, jsonify
from encryption import encrypt_data, decrypt_data
from models import MedicalRecord, db
from api.routes import api_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_records.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
app.register_blueprint(api_routes)

@app.route('/')
def home():
    return "Welcome to the Privacy-Preserving Medical Records Platform!"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
