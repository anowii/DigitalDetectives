import json
import os
import pandas as pd
from langchain_ollama import OllamaLLM
from templates import json_template, simple_template, sql_template
from diskanalys import run

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

def send_query_to_db(query):
    success = True
    response = query
    return response, success

# Function to handle message forwarding to LLM
def forward_message_llm(message, filepath):
    # Load previous conversation history

    json_data = load_json_data(filepath)  # Initialize JSON data as empty
    print(f"JSON Data: {json_data}")  # Log the JSON data

    # Determine weather to invoke sql agent or json chain (determining this using llm is too much trouble for what its worth)
    if message.lower().startswith("list"):
        print("List detected in question running sql agent")
        query = chain_sql.invoke({"question": message})
        result, sql_success = send_query_to_db(query)

    # If sql query fails or it dosn't start with "list" answer the question normally with json data
    if sql_success == False or message.lower().startswith("list") == False:
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
