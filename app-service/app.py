import os
from flask import Flask, request, render_template_string, redirect, url_for
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Get the connection string from the environment variable (set in App Service Configuration)
connect_str = os.getenv('StorageConnectionString')
if not connect_str:
    raise ValueError("Azure Storage Connection String not found in environment variables.")

# Create the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "originals" # The container we upload to

# A simple HTML template for the upload form
HTML_TEMPLATE = """
<!doctype html>
<title>Uplift - Image Uploader</title>
<style>
  body { font-family: sans-serif; background: #f4f7f6; display: grid; place-items: center; min-height: 90vh; }
  .card { background: #fff; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); padding: 2rem; width: 350px; text-align: center; }
  h1 { color: #333; }
  input[type=file] { margin: 1rem 0; }
  input[type=submit] { 
    background: #0078d4; color: white; border: none; padding: 10px 20px; 
    border-radius: 8px; cursor: pointer; font-size: 16px; transition: background 0.2s;
  }
  input[type=submit]:hover { background: #005a9e; }
  .message { margin-top: 1rem; color: #28a745; font-weight: bold; }
</style>
<div class="card">
  <h1>Upload New Image</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <input type=submit value=Upload>
  </form>
  {% if message %}
    <p class="message">{{ message }}</p>
  {% endif %}
</div>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            try:
                # Create a blob client using the original filename
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
                
                # Upload the file
                blob_client.upload_blob(file, overwrite=True)
                message = f"File '{file.filename}' uploaded successfully!"
            except Exception as e:
                message = f"An error occurred: {str(e)}"

    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(debug=True)
