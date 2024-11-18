
from flask import Flask, render_template, request, jsonify,redirect,url_for, json, session, flash, send_file

import os
import io
import hashlib
from diskanalys import create_database_from_csv
from ui_backend import send_iso,forward_message_llm, is_valid_disk_image, generate_pdf, delete_session



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
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return redirect(url_for('chat'))

@app.route('/login')      #CURRENTLY NOT WORKING, SHOULD REDIRECT USER TO HOME WHEN PRESSING SUBMIT (TEMPORARY WHEN NO LOGIN DETAILS)
def login():
    return render_template('login.html')


# Login handling
@app.route('/login', methods=['POST'])      #CURRENTLY NOT WORKING, SHOULD REDIRECT USER TO HOME WHEN PRESSING SUBMIT (TEMPORARY WHEN NO LOGIN DETAILS)
def login_post():
    result = request.form['password']
    result = hashlib.md5(result.encode())
    result = result.hexdigest()
    user = request.form['username']
    
    #default users
    #user = password
    #admin = muchmoresecure
    Users = {"user":"5f4dcc3b5aa765d61d8327deb882cf99", "admin":"0c768dfef098837ed8a1ea70be211e38"}

    if user in Users:
        if result == Users[user]:
            session['logged_in'] = True
            session['username'] = user  # Store the username in the session
            return home()
        else:
            flash('Wrong password or Username', 'error')
    else:
        flash('Wrong password or Username', 'error')

    return home()



@app.route('/logout', methods=['POST'])
def logout_post():
    if session['logged_in'] == False:
        session.pop('username', None)
        return redirect(url_for('home'))
    else:
        session['logged_in'] = False
        return redirect(url_for('home'))


# Home page 
@app.route('/home')
def chat():
    if not session.get('logged_in'):
        return home()
    
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
    
    # Call different functions based on file type
    if file.filename.endswith('.csv'):
        global UPLOADED_CSV
        UPLOADED_CSV = file_path
        create_database_from_csv(UPLOADED_CSV)

    elif is_valid_disk_image(file_path) == True:
        send_iso(file_path)  # Call ISO handling function with file path
        UPLOADED_CSV = 'data\\db.csv'
    else:
        print("Non-valid file type")

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

        # Mostly for logging/debug purposes
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

@app.route('/download_chat', methods=['GET'])
def download_chat():
    pdf_buffer = generate_pdf(messages)
    return send_file(pdf_buffer,as_attachment=True,download_name="chat_history.pdf",mimetype="application/pdf")

@app.route('/delete_session', methods=['POST'])
def delete_session_route():
    global messages, UPLOADED_CSV

    # Call the delete_session function from ui_backend
    return delete_session(messages, UPLOADED_CSV)

def main():
    app.secret_key = os.urandom(12)
    app.run('localhost', 5000)
    

if __name__ == '__main__':
    main()
    

