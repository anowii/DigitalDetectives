from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
def login():
    return render_template('login.html')

# Route to handle file name submission via AJAX
@app.route('/submit-file', methods=['POST'])
def submit_file():
    file_name = request.form.get('filename')  # Get the file name from the AJAX request
    print(f"Received file name: {file_name}")
    
    # You can now store the file name in a variable or process it as needed
    # Return a response to the client
    return jsonify({"status": "success", "filename": file_name})

if __name__ == '__main__':
    app.run(threaded=True, port=4994)