from flask import Flask, render_template, request, jsonify
from ui_backend import send_iso, send_csv

app = Flask(__name__)

@app.route('/home')
def home():
    send_iso()
    return render_template('index.html')

@app.route('/')
def login():
    return render_template('login.html')



# Route to handle file name submission via AJAX
@app.route('/submit-file', methods=['POST'])
def submit_file():
    file_name = request.form.get('filename')  # Get the file name from the AJAX request
    print(f"Received file name: {file_name}")
    
    if(file_name.endswith('.csv')):
        send_csv(file_name) #ADD HANDLING FOR CSV
    elif(file_name.endswith('.iso')):
        send_iso(file_name) #ADD HANDLING FOR ISO
    else:
        print("non valid file type")

    # Return a response to the client
    return jsonify({"status": "success", "filename": file_name})

def main():
    app.run(threaded=True, port=4987)
    return 0

if __name__ == '__main__':
    main()