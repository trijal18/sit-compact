class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_records.db'  # Use SQLite or another database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # Change to a more secure key in production
    JWT_SECRET_KEY = 'your_jwt_secret_key'
