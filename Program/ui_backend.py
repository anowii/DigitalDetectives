import json
import os
import pandas as pd
from langchain_ollama import OllamaLLM
from templates import json_template, simple_template, sql_template
from diskanalys import run, USER_DB, create_database_from_csv
import sqlite3
from tabulate import tabulate


model = OllamaLLM(model="llama3.2")
#chain = json_template | model
chain = simple_template | model
chain_sql = sql_template | model

# Load CSV data from filename/filepath returns it in JSON format 
def load_json_data(filename):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)

            # Ensure the column headers match expected structure
            df.columns = ['name', 'size', 'crtime', 'path', 'virus', 'virus_type']

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

def send_query_to_db(query):
    print("Query: ", query)
    # Connect to the db
    success = True
    try:
        con = sqlite3.connect(USER_DB)
        cursor = con.cursor()
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return "", False, []
    
    # Query the DB
    try: 
        cursor.execute(query)
        response = cursor.fetchall()
        # Get headers
        column_headers = [description[0] for description in cursor.description]
    except sqlite3.Error as e:
        print(f"An error occurred while querying the database: {e}")
        return "", False, []
    return response, success, column_headers

# Function to handle message forwarding to LLM
def forward_message_llm(message, filepath):
    # Load previous conversation history
    
    json_data = load_json_data(filepath)  # Initialize JSON data as empty
    print(f"JSON Data: {json_data}")  # Log the JSON data

    # Determine weather to invoke sql agent or json chain (determining this using llm is too much trouble for what its worth)
    if message.lower().startswith("list"):
        print("List detected in question: running sql agent")
        query = chain_sql.invoke({"question": message})
        result, sql_success, column_headers = send_query_to_db(query)
        if sql_success:
            
            result = "Result generated from " + query + ":<br><br>" + db_response_to_html(result, column_headers).replace("\n", "")

    # If sql query fails or it dosn't start with "list" answer the question normally with json data
    if message.lower().startswith("list") == False or sql_success == False:
        result = chain.invoke({"json_data": json_data ,"question": message})
    
    # Use Langchain chain to get AI response
    
    #print('bye')
    
    return result

def send_iso(fileName): #Runs TSK on disk image file (".dd")
    run(fileName)
    print(fileName)
    return 0

def is_valid_disk_image(disk_image):
    """
    Checks if a given disk image path is valid by verifying its file extension.
    Returns True if the file extension is valid, False otherwise.
    """
    #valid_extensions =[".img",  ".iso", ".vdi", ".vmdk", ".vhd", ".dmg",".qcow2", ".dd"] # Add more file types
    valid_extensions = [".dd"]
    _,ext = os.path.splitext(disk_image)
    if ext.lower() not in valid_extensions:
        return False

    return True
