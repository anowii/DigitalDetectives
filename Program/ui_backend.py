import pandas as pd
from langchain_ollama import OllamaLLM
from templates import json_template2, sql_template, sql_correction_template, simple_template
from diskanalys import run, USER_DB
from tabulate import tabulate
from flask import jsonify

import csv,json
from io import BytesIO, StringIO #chat download
from reportlab.lib.pagesizes import letter #chat download
from reportlab.lib.styles import getSampleStyleSheet #chat download
import html, os, sqlite3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer #chat download
from bs4 import BeautifulSoup
MESSAGE_FILE = 'messages.json'


model = OllamaLLM(model="llama3.2")
chain_simple = simple_template | model
chain = json_template2 | model
chain_sql = sql_template | model
chain_sql_correction = sql_correction_template | model
use_default_json = True
query_json_data = ""


# Helper function to save a message to the file
def save_message_to_file(message_object):
    with open(MESSAGE_FILE, 'a') as f:
        f.write(json.dumps(message_object) + '\n')


# Load CSV data from filename/filepath returns it in JSON format 
def load_json_data(filename):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)

            # Ensure the column headers match expected structure
            df.columns = ['name', 'size', 'crtime', 'path', 'malware_class','delete_flag']

            # Convert to JSON string
            return df.to_dict(orient='records') 
        except pd.errors.EmptyDataError:
            print("File is empty or incorrect.")
            return []
        except pd.errors.ParserError as e:
            print(f"Error parsing: {e}")
            return []
    else:
        print("File does not exist.")
        return []

  
def db_response_to_html(response, column_headers):
    if not response:
        return "No result"
    else:
        # Format the result
        print(response)
        text = tabulate(response, headers=column_headers, tablefmt="html", numalign="left")
        print(text)
        return text
    
def set_use_defualt_json(): # should be called by context_btn.js
    global use_default_json
    use_default_json = True
    print("Switching to Default json")
    
    
def reset_use_default_json(): # should be called by context_btn.js
    global use_default_json
    use_default_json = False
    print("Switching to Modifed json")
    return

def query_to_json(query): # Not done should be called by context_btn.js
    response, success, column_headers = send_query_to_db(query)
    
    if success:
        # Turn data into json format
        json_content = "["
        json_content += ",".join(
            "{" + ",".join(f'"{key}": "{value}"' for key, value in zip(column_headers, row)) + "}"
            for row in response
        )
        json_content += "]"
        global query_json_data
        query_json_data = json_content
    else:
        print("Query Failed")

def send_query_to_db(query):
    print("Query: ", query)
    if query.lower().startswith("select") == False: # Select check
        return "Error: query has to be a select", False, []
    # Connect to the db
    try:
        con = sqlite3.connect(USER_DB)
        cursor = con.cursor()
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return "", False, []
    # Query the DB
    try: 
        cursor.execute("SELECT * FROM sqlite_master")
        print("tables:", cursor.fetchall())
        cursor.execute(query)
        response = cursor.fetchall()
        # Get headers
        column_headers = [description[0] for description in cursor.description]
    except sqlite3.Error as e:
        print(f"An error occurred while querying the database: {e}")
        con.close()
        return e, False, []
    con.close()
    return response, True, column_headers

def call_sql_agent(message):
    query = chain_sql.invoke({"question": message})
    result, sql_success, column_headers = send_query_to_db(query)
    if sql_success:
        result = "Result generated from " + query + ":<br><br>" + db_response_to_html(result, column_headers).replace("\n", "")
    elif result != "": # Try again (empty result means db connection failed)
        print(query, "failed asking LLM to correct it")
        query = chain_sql_correction.invoke({"query": query, "error": result})
        result, sql_success, column_headers = send_query_to_db(query)
        if sql_success:
            result = "Result generated from " + query + ":<br><br>" + db_response_to_html(result, column_headers).replace("\n", "")
    return result, sql_success

# Function to handle message forwarding to LLM
def forward_message_llm(message, filepath):
    global use_default_json
    global query_json_data

    json_data = load_json_data(filepath) 
    print(f"JSON Data: {json_data}")  # Log the JSON data to terminal
    try:
        # Determine weather to invoke sql agent or json chain
        if message.lower().startswith("list"):
            print("List detected in question: running sql agent")
            result, sql_success = call_sql_agent(message)

        # If sql query fails or it dosn't start with "list" answer the question normally with json data
        if message.lower().startswith("list") == False or sql_success == False:
            print("Use default json is:", use_default_json)
            if use_default_json:
                result = chain.invoke({"json_data": json_data ,"question": message})
            else:
                result = chain_simple.invoke({"json_data": query_json_data ,"question": message}) 
    except Exception as e:
        print(f"Error: {e}")
        result = "Unable to connect to your AI. Please make sure your model is up and running."
    return result


def send_iso(fileName): #Runs TSK on disk image file (".dd")
    run(fileName)
    print(f"Disk image {fileName} processed successfully.")
    
    return 0 



def is_valid_disk_image(disk_image):
    """
    Checks if a given disk image path is valid by verifying its file extension.
    Returns True if the file extension is valid, False otherwise.
    """
    #valid_extensions =[".img",  ".iso", ".vdi", ".vmdk", ".vhd", ".dmg",".qcow2", ".dd"] # Add more file types depending on usage
    valid_extensions = [".dd"]
    _,ext = os.path.splitext(disk_image)
    if ext.lower() not in valid_extensions:
        return False

    return True

#Generate a PDF of chat messages for download
def generate_pdf(messages):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    title = Paragraph("Chat History", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Function to sanitize HTML and replace <br> with newlines
    def sanitize_html(input_html):
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(input_html, "html.parser")

        # Replace <br> tags with newline characters
        for br_tag in soup.find_all("br"):
            br_tag.insert_after("\n")
            br_tag.unwrap()  # Remove the <br> tag itself

        # Strip all other tags (except the <br> processed ones)
        return soup.get_text()

    # Add messages
    for msg in messages:
        # Clean and format user and AI messages
        user_message = f"User ({msg['id']}): {sanitize_html(msg['user'])}"
        ai_response = f"AI: {sanitize_html(msg['response'])}"

        user_message = html.escape(user_message)
        ai_response = html.escape(ai_response)

        # Add messages to PDF
        elements.append(Paragraph(user_message, styles["BodyText"]))
        elements.append(Spacer(1, 10))  # space between messages
        elements.append(Paragraph(ai_response, styles["BodyText"]))
        elements.append(Spacer(1, 20))  # space between entries

    # Build the PDF
    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer

#Delete session data handling
def delete_session(messages, uploaded_csv_path):
    # Clear messages array
    global use_default_json
    use_default_json = True
    messages.clear()
    uploaded_csv_path = ''

    return jsonify({"status": "success", "message": "Session cleared successfully"})