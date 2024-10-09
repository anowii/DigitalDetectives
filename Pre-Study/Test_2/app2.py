# Imports various modules from the Flask web framework
from flask import Flask, redirect, url_for, render_template, session, request, get_flashed_messages, jsonify

# Import OS, Subprocesses, CSV, and ollama modules
import os
import subprocess
import csv
import ollama

#  Create a new Flask application instance
app = Flask(__name__)

# Set a secrte key for the application, which is used
# to sign the session cookie and protect it from tampering
app.secret_key = 'mysecretkey'  

# This the home page route, which handles both GET and
# POST requests. It renders the home.html template.
@app.route("/", methods=["Get", "POST"])
def home():
    """
    Handles the home page, which accepts a disk image path as input.
    If the input is valid, it redirects to the process page.
    If the input is invalid, it displays an error message on the home page.
    """
    if request.method == "POST":
        disk_image = request.form["disk_image"]
        if is_valid_disk_image(disk_image):
            print("Disk image is valid!")
            session["disk_image"] = disk_image
            print("Session disk_image: ", session["disk_image"])

            response = redirect(url_for("process"))
            print("Redirecting to process page ...")
            return response
        else:
            error_message = "Invalid disk image.  Please enter a valid disk image path"
            return render_template("home.html", error_message=error_message)

    return render_template("home.html", chat_window=True)




def is_valid_disk_image(disk_image):
    """
    Checks if a given disk image path is valid by verifying its file extension.
    Returns True if the file extension is valid, False otherwise.
    """
    valid_extensions =[".img",  ".iso", ".vdi", ".vmdk", ".vhd", ".dmg",
                       ".qcow2",".dd"] # Add more file types
    _,ext = os.path.splitext(disk_image)
    if ext.lower() not in valid_extensions:
        return False

    return True

@app.route('/clear_session')
def clear_session():
    """
    Clears the current session and redirects to the home page.
    """
    session.clear()
    return redirect(url_for('home'))

@app.route("/process")
def process():
    """
    Retrieves the disk image from the session, runs the fls command to list files,
    and generates a CSV file with the file information.
    Displays a success message on the process page if successful, or an error message otherwise.
    """

    # Retrieve the disk_image from the session
    disk_image = session.get('disk_image')

    # Check if disk_image is valid
    if disk_image is None:
        # Display an error message on process page
        return redirect(url_for("home"))
    
    try:
        # Example command to list files using sleuth kit's fls
        command = ['fls', '-r', session["disk_image"]] 
        print("Hi fls -r ", command)
       
        result = subprocess.run(command, capture_output=True, text=True, cwd=os.path.dirname(disk_image))
        print("fls is don")

        output = ""
        # Check if the command was successful
        if result.returncode == 0:
           
            # Check if the ouptut is empty
            output = result.stdout
            print("fls have and output: ", output)

            if not output.strip(): # Use strip() to remove leading/trailing whitspaces
                error_message = "No output from fls command"
                return render_template("process.html", error_message=error_message)

            # Parse the output to extract file information
            file =[]
            for line in output.splitlines():
                if line.startswith('+ ') or line.startswith('++ ') or line.startswith('+++ '):
                    columns = line.split()
                    file_type = columns[1][1:] # Remove the '+' or '++' or '++' prefix
                    file_name = ' '.join(columns[2:])
                    file.append({'File Name': file_name,  'File Type': file_type})
            
            # Convert the list of dictionaries into a csv file
            csv_filename ='ouput.csv'
            csv_pth = os.path.join(os.path.dirname(disk_image), csv_filename)
              
            with open(csv_pth, 'w', newline='') as csvfile:
                csvfile.write("Number,Name,Type,Path\n")
                for line in output.splitlines():
                    if line.startswith('+ ') or line.startswith('++ ') or line.startswith('+++ '):
                        columns = line.split()
                        number = columns[0]
                        file_type = columns[1][1:]  # Remove the '+' or '++' or '+++' prefix
                        file_name = ' '.join(columns[2:])
                        file_path = os.path.join(os.path.dirname(disk_image), file_name)
                        csvfile.write(f"{number},{file_name},{file_type},{file_path}\n")
            # Display a success message on the progress page
            success_message = f"Processing complete. CSV file saved to {csv_pth}. Cleare Session and Go Home"
            return render_template("process.html", success_message=success_message)

        else:
            # Display an error message on process page
            error_message =  f"Error processing disk image (returncode {result.returncode})"
            return render_template("process.html", error_message=error_message)
    except Exception as e:
        error_message =  f"An error occurred: {e}"
        return render_template("process.html", error_message=error_message)
   


MAX_TOKENS = 2048  # Adjust based on your model's token limit

@app.route("/llm_response", methods=["POST"])
def llm_response():
    if 'message_history' not in session:
        session['message_history'] = []

    input_text = request.json.get("input")
    if not input_text:
        return jsonify({"response": "Error: Input text is empty."})

    # Append the new user message to the session history
    session['message_history'].append({"role": "user", "content": input_text})

    # Check if the history size exceeds the token limit
    total_tokens = sum([len(message['content']) for message in session['message_history']])
    if total_tokens > MAX_TOKENS:
        session['message_history'] = session['message_history'][-10:]  # Keep only the last 10 messages

    try:
        # Include the message history in the payload
        response = ollama.chat(model="llama3.1:8b", messages=session['message_history'])

        response_text = response.get('message', {}).get('content', "Error: Unable to generate a response.")

        # Append the model's response to the session history
        session['message_history'].append({"role": "assistant", "content": response_text})

    except Exception as e:
        response_text = f"Error: {str(e)}"

    return jsonify({"response": response_text})

# Runs the Flask application in debug mode if the
# the script executed directly (i.e., not imported as a madule)
if __name__ == "__main__":
    
    app.run(debug=True)
