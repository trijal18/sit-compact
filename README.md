# Privacy-Preserving Medical Records Platform

This project is a secure platform for sharing sensitive medical records between users and trusted entities while maintaining privacy. It uses advanced encryption techniques such as **Homomorphic Encryption** and **Differential Privacy** to protect data confidentiality.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Dockerization (Optional)](#dockerization-optional)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Technologies Used
- **Backend**: Python, Flask, AES/RSA Encryption, Homomorphic Encryption, Differential Privacy
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite/MySQL
- **Docker**: For containerization

## Setup and Installation

### Backend Setup

#### Step 1: Install Dependencies
1. Navigate to the backend directory and create a virtual environment:
    ```bash
    cd backend
    python3 -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
3. Install the necessary Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

#### Step 2: Set Up the Database
1. Initialize the database by running the `init_db.py` script:
    ```bash
    python database/init_db.py
    ```

#### Step 3: Run the Flask Application
1. Start the Flask backend:
    ```bash
    python app.py
    ```
2. The server will start on `http://localhost:5000`.

---

### Frontend Setup

#### Step 1: Serve the Frontend Files
You can either serve the frontend using Python's HTTP server or directly from Flask.

**Option 1: Using Python's HTTP Server**
1. Navigate to the `frontend/` directory:
    ```bash
    cd frontend
    ```
2. Run a simple HTTP server:
    ```bash
    python -m http.server 8000
    ```
3. The frontend will be accessible at `http://localhost:8000`.

**Option 2: Host Frontend with Flask (Optional)**
1. If you prefer to serve the frontend from the Flask backend, modify `app.py` to serve static files from the `frontend/` folder.
2. Restart Flask, and the frontend will be served at `http://localhost:5000`.

---

### Dockerization (Optional)

#### Step 1: Build the Docker Image
1. In the project root directory, create a Docker image:
    ```bash
    docker build -t medical-records-app .
    ```

#### Step 2: Run the Docker Container
1. Run the container:
    ```bash
    docker run -p 5000:5000 -p 8000:8000 medical-records-app
    ```

---

## Running the Application

Once the backend and frontend are running:

- **Frontend**: Open your browser and go to `http://localhost:8000` (if using Python's HTTP server) or `http://localhost:5000` (if using Flask to serve frontend).
- **Backend**: The API will be available at `http://localhost:5000`.

---

## Testing the Application

1. **Register or Login**: Go to the platform and register a new user or log in with existing credentials.
2. **Upload Medical Record**: After logging in, navigate to the "Upload Medical Record" page and submit the data.
3. **Test API Endpoints (Optional)**: You can test the backend APIs using tools like Postman or curl:
    - **Login API**: `POST /api/login` with `{ "username": "your_username", "password": "your_password" }`
    - **Upload API**: `POST /api/upload` with the data and a valid JWT token in the Authorization header.

---

## Troubleshooting

- **Ensure Dependencies Are Installed**: Make sure you've installed all required dependencies in both frontend and backend environments.
- **Database Issues**: If the database isn't initializing correctly, check the database configuration in `config.py`.
- **Cross-Origin Requests (CORS)**: If you face CORS issues, consider using the `flask-cors` package in the backend.

---

