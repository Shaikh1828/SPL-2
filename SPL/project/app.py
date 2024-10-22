from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database configuration for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'apk'}

# Function to check if file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database Model for storing file details
class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# # Create the database (run this only once)
# with app.app_context():
#     db.create_all()

# Route to display the file upload form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If user does not select a file, browser may submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the file to the uploads directory
            try:
                # Save file to disk
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Save file information to the database
                new_file = UploadedFile(filename=filename, filepath=filepath)
                db.session.add(new_file)
                db.session.commit()
                
                return f'File successfully uploaded: {filename}', 200

                flash('File successfully uploaded and saved to the database')
            except Exception as e:
                db.session.rollback()  # Rollback in case of any error
                flash(f'Error saving file: {e}')
        else:
            return 'Invalid file type', 400

    # Render the HTML form for file upload
    return render_template('index.html')

# Start the server
if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Run this once
    app.run(debug=True)
