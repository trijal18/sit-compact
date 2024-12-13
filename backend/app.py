from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash
import os

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Configure the upload folder
UPLOAD_FOLDER = 'backend/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'docx', 'xlsx'}

def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home route to display the upload form and list files."""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    if 'file' not in request.files:
        flash('No file part in the request.')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected for uploading.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'File {filename} uploaded successfully.')
        return redirect(url_for('index'))
    else:
        flash('File type not allowed.')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Handle file downloads."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Delete a file from the server."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'File {filename} deleted successfully.')
    else:
        flash(f'File {filename} not found.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
