from flask import Flask, request, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

# Set the directory for uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'No file part'
            return render_template('upload.html', message=message)
        
        file = request.files['file']
        
        if file.filename == '':
            message = 'No selected file'
            return render_template('upload.html', message=message)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            message = f'File {filename} uploaded successfully!'
            return render_template('upload.html', message=message)
        else:
            message = 'File type not allowed'
            return render_template('upload.html', message=message)
    return render_template('upload.html')

# Route to handle file download
@app.route('/download', methods=['GET'])
def download():
    filename = request.args.get('filename')
    if not filename:
        error = 'Filename is required'
        return render_template('download.html', error=error)
    
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        error = 'File not found'
        return render_template('download.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
