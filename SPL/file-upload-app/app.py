from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Path to the directory where files will be uploaded
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'apk'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request has the file part
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return 'No selected file', 400

    # If the file is allowed, save it to the uploads folder
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return f'File successfully uploaded: {filename}', 200
    
    return 'Invalid file type', 400

if __name__ == '__main__':
    app.run(debug=True)
