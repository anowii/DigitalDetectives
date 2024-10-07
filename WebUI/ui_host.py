from flask import Flask, render_template, request, jsonify
import os
from ui_backend import send_iso, send_csv

app = Flask(__name__)

UPLOAD_FOLDER = 'tempfiles'  # Designated folder name
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def login():
    return render_template('login.html')





# Route to handle file upload
@app.route('/submit-file', methods=['POST'])
def submit_file():
    # Check if upload folder exists; otherwise, create it
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Check if the file part is present
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})

    file = request.files['file']  # Get the uploaded file

    # Check if a file was selected
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})

    # Save file to tempfiles directory
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    print(f"Received file: {file.filename}")





    #If a filename match to already uploaded files to local tempfolder then dont upload or smthng

    # Call different functions based on file type
    if file.filename.endswith('.csv'):
        send_csv(file_path)  # Call CSV handling function with file path
    elif file.filename.endswith('.iso'):         
        send_iso(file_path)  # Call ISO handling function with file path
    else:
        print("Non-valid file type")








    # Return a response to the client
    return jsonify({"status": "success", "filename": file.filename})

def main():
    app.run(threaded=True, port=4984)
    return 0

if __name__ == '__main__':
    main()