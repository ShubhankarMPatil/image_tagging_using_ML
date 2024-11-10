import os
import json
from flask import Flask, request, render_template, redirect, url_for
from main import process_images_from_directory  # Importing the function from main.py

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'test_images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the main page to select the directory
@app.route('/')
def index():
    return render_template('index.html')

# Route to process images
@app.route('/process_images', methods=['POST'])
def process_images():
    # Clear any existing files in the upload folder
    # if os.path.exists(app.config['UPLOAD_FOLDER']):
    #     for filename in os.listdir(app.config['UPLOAD_FOLDER']):
    #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #         os.remove(file_path)

    # # Save uploaded files to the upload folder
    # for uploaded_file in request.files.getlist("directory"):
    #     if uploaded_file.filename != '':
    #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    #         uploaded_file.save(file_path)

    # Process images and store results in a JSON file
    process_images_from_directory(app.config['UPLOAD_FOLDER'])

    # Redirect to the results page to display processed images and tags
    return redirect(url_for('results'))

# Route to display results
@app.route('/results')
def results():
    with open('image_data.json', 'r') as file:
        data = json.load(file)
    return render_template('results.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
