from flask import Flask, render_template, request, jsonify
import os
from ui_backend import send_iso, send_csv, forward_message_llm

app = Flask(__name__)

UPLOAD_FOLDER = 'tempfiles'  # Designated folder name
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Store chat messages in memory for now (could use a database instead)
messages = []

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






# Route to handle chat message submission
@app.route('/forward_message', methods=['POST'])
def forward_message():
    data = request.get_json()  # Get the JSON data from the request
    message = data.get('message', '')  # Extract the message

    if message:
        forward_message_llm(message)  # Call the function to process the message
        messages.append(message)  # Store the message
        return jsonify({'status': 'success', 'message': 'Message forwarded'})
    else:
        return jsonify({'status': 'error', 'message': 'No message received'})



# Route to retrieve new messages
@app.route('/get_messages', methods=['GET'])
def get_messages():
    # Return the list of messages to the client
    return jsonify(messages)


def main():
    app.run(threaded=True, port=4980)
    return 0

if __name__ == '__main__':
    main()