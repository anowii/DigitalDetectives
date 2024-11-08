
from flask import Flask, render_template, request, jsonify,redirect,url_for, json
import os
from ui_backend import send_iso,forward_message_llm, is_valid_disk_image

app = Flask(__name__)
#app.secret_key = "The Secret key"

UPLOAD_FOLDER = 'data'  # Designated folder name
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOADED_CSV = '' #filepath for CSV

# Store chat messages in memory for now, per session
messages = []
MESSAGE_FILE = 'messages.json'
next_id = 1  # Initialize the message ID

# Default route 
@app.route('/')
def login():
    return render_template('login.html')

# Login handling
@app.route('/login', methods=['POST'])      #CURRENTLY NOT WORKING, SHOULD REDIRECT USER TO HOME WHEN PRESSING SUBMIT (TEMPORARY WHEN NO LOGIN DETAILS)
def handle_login():
    return redirect(url_for('home'))

# Home page 
@app.route('/home')
def home():
    return render_template('home.html')

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

    # Save file to data directory
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    print(f"Received file: {file.filename}")


    #If a filename match to already uploaded files to local tempfolder then dont upload or smthng
    
    # Call different functions based on file type
    if file.filename.endswith('.csv'):
        global UPLOADED_CSV
        UPLOADED_CSV = file_path

    elif is_valid_disk_image(file_path) == True:
        send_iso(file_path)  # Call ISO handling function with file path
    else:
        print("Non-valid file type") #Do something more??????????

    # Return a response to the client
    return jsonify({"status": "success", "filename": file.filename})

# Helper function to save a message to the file
def save_message_to_file(message_object):
    with open(MESSAGE_FILE, 'a') as f:
        f.write(json.dumps(message_object) + ',\n')

# Forwards message to LLM
@app.route('/forward_message', methods=['POST'])
def forward_message():
    global next_id
    data = request.get_json()  # Get JSON data from request
    message = data.get('message', '')  # Extract the message

    if message:
        response = forward_message_llm(message,UPLOADED_CSV)  # Forward to Langchain-based LLM
        
        # Mostly for loggin/debug purposes 
        message_object = {
            "id": next_id, 
            "csv": UPLOADED_CSV if UPLOADED_CSV else "empty",
            "user": message,
            "response": response
        }

        # Append message and response to the chat history
        messages.append({"id": next_id, "user": message, "response": response})

        # Mostly for loggin/debug purposes
        save_message_to_file(message_object)
        next_id += 1      

        return jsonify({'status': 'success', 'message': response})
    else:
        return jsonify({'status': 'error', 'message': 'No message received'})


# Get messages
@app.route('/get_messages', methods=['GET'])
def get_messages():
    # Return the list of user messages and LLM responses to the client
    return jsonify(messages)

def main():
    app.run(debug=True, threaded=True, port=4976)

if __name__ == '__main__':
    main()
    

