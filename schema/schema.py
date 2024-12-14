from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/healthcare_db"
mongo = PyMongo(app)

# Define Doctor Schema
doctor_schema = {
    "name": {
        "type": "string",
        "required": True
    },
    "patients": {
        "type": "array",
        "default": []
    },
    "speciality": {
        "type": "string",
        "required": True
    }
}

# Define Patient Schema
patient_schema = {
    "name": {
        "type": "string",
        "required": True
    },
    "doctors": {
        "type": "array",
        "default": []
    }
}

# Define Public Key Schema
public_key_schema = {
    "public_key": {
        "type": "string",
        "required": True
    }
}

if __name__ == "__main__":
    app.run(debug=True)
