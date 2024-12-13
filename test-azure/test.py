from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError

app = Flask(__name__)

# Initialize Azure Blob service client using your connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=shareencrypt;AccountKey=KvutLtrtXl0b6nuC+W29ABje2ZpHm7yyMBKcdcCIOOIbs2u0rkzSb61vRtJ07qeK8GCJBf7/9qRh+AStGam16Q==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Define the container name
CONTAINER_NAME = "store"

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    return render_template('download_file.html')
# Route to read a file from Azure Blob Storage
@app.route('/download_file', methods=['GET'])
def read_file():
    file_name = request.args.get('file_name')

    if not file_name:
        return jsonify({'error': 'No file name provided'}), 400

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)
        
        # Download the blob data
        blob_data = blob_client.download_blob()
        file_content = blob_data.readall().decode('utf-8')

        return jsonify({'file_content': file_content})

    except ResourceNotFoundError:
        return jsonify({'error': f'File {file_name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/upload')
def upload():
    return render_template('upload_file.html')
# Route to write a file to Azure Blob Storage
@app.route('/upload_file', methods=['POST'])
def write_file():
    file_name = request.form.get('file_name')
    file_content = request.form.get('file_content')

    if not file_name or not file_content:
        return jsonify({'error': 'File name and content are required'}), 400

    try:
        # Get a reference to the blob (file)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        # Upload the blob data (file content)
        blob_client.upload_blob(file_content, overwrite=True)

        return jsonify({'message': f'File {file_name} uploaded successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
