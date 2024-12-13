from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from encryption.file import encrypt_file, decrypt_file
app = Flask(__name__)

# Set the directory for uploaded files
OG_UPLOAD_FOLDER = 'og_uploads'
SEXY_UPLOAD_FOLDER='sexy_uploads'
if not os.path.exists(OG_UPLOAD_FOLDER):
    os.makedirs(OG_UPLOAD_FOLDER)
if not os.path.exists(SEXY_UPLOAD_FOLDER):
    os.makedirs(SEXY_UPLOAD_FOLDER)

app.config['OG_UPLOAD_FOLDER'] = OG_UPLOAD_FOLDER
app.config['SEXY_UPLOAD_FOLDER'] = SEXY_UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

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
            #function to encrpt file 
            og_file=os.path.join(app.config['OG_UPLOAD_FOLDER'], filename)
            file.save(og_file)
            sexy_file=os.path.join(app.config['SEXY_UPLOAD_FOLDER'], filename)
            key=encrypt_file(og_file,sexy_file)
            message = f'File {filename} uploaded successfully!'
            return render_template('display_key.html', key=key)# redirect to secret key
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
        #func to decrpt file
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        error = 'File not found'
        return render_template('download.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
