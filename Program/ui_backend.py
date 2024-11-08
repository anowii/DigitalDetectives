import json
import os
import pandas as pd
from langchain_ollama import OllamaLLM
from templates import json_template, simple_template
from diskanalys import run

model = OllamaLLM(model="llama3.2")
#chain = json_template | model
chain = simple_template | model


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


# Function to handle message forwarding to LLM
def forward_message_llm(message, filepath):

    # Load JSON data from 'current csv file'
    json_data = load_json_data(filepath) 
    print(f"JSON Data: {json_data}")    # Print for debug/checking purposes only
  
    # Use Langchain chain to get AI response
    result = chain.invoke({"json_data": json_data ,"question": message})
    
    return result  # Return the result to be used in Flask

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
