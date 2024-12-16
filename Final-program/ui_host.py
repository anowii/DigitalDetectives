#Application hosting and handling for flask

from flask import Flask, render_template, request, jsonify,redirect,url_for, json, session, flash, send_file

import os
import hashlib
from diskanalys import create_database_from_csv
from ui_backend import send_iso,forward_message_llm, is_valid_disk_image, generate_pdf, delete_session, set_use_defualt_json, reset_use_default_json, query_to_json
from ui_backend import save_message_to_file



app = Flask(__name__)
#app.secret_key = "The Secret key"

UPLOAD_FOLDER = 'data'  # Designated folder name
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOADED_CSV = '' #filepath for CSV

# Store chat messages in memory for now, per session
messages = []
next_id = 0  # Initialize the message ID

# Default route 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return redirect(url_for('chat'))

#Login route
@app.route('/login')      
def login():
    return render_template('login.html')


# Login handling
@app.route('/login', methods=['POST'])      
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


#Logout handling
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
        return jsonify({"status": "success", "message": "CSV file Loaded: ", "filename": file.filename})

    elif is_valid_disk_image(file_path) == True:
        send_iso(file_path)  # Call ISO handling function with file path
        UPLOADED_CSV = 'data\\db.csv'
        return jsonify({"status": "success", "message": "Disk image processed successfully", "filename": file.filename})
    else:
        return jsonify({"status": "error", "message": "Invalid file type. Please upload a valid file."})

# Forwards message to LLM
@app.route('/forward_message', methods=['POST'])
def forward_message():
    global next_id
    data = request.get_json()  # Get JSON data from request
    message = data.get('message', '')  # Extract the message

    if message:
        response = forward_message_llm(message,UPLOADED_CSV)  # Forward to Langchain-based LLM
        
        #logging/debug
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

#Agent handling
@app.route('/set_json_data', methods=['POST'])
def set_query_data():
    data = request.json
    query = data.get('query', '')
    reset_use_default_json()
    query_to_json(query)
    return jsonify({"status": "success", "message": "Query data set"})

@app.route('/reset_json_data', methods=['POST'])
def reset_query_data():
    set_use_defualt_json()
    return jsonify({"status": "success", "message": "Query data reset"})

#Download chat handling
@app.route('/download_chat', methods=['GET'])
def download_chat():
    pdf_buffer = generate_pdf(messages)
    return send_file(pdf_buffer,as_attachment=True,download_name="chat_history.pdf",mimetype="application/pdf")

#Delete session handling
@app.route('/delete_session', methods=['POST'])
def delete_session_route():
    global messages, UPLOADED_CSV

    # Call the delete_session function from ui_backend
    return delete_session(messages, UPLOADED_CSV)


@app.route('/set query_data')
def main():
    app.secret_key = os.urandom(12)
    app.run('localhost', 5000,debug=True)
    

if __name__ == '__main__':
    main()