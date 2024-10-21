import json
import os
import pandas as pd
from langchain_ollama import OllamaLLM
from templates import json_template, simple_template


model = OllamaLLM(model="llama3.1:8b")
chain = json_template | model
#chain = simple_template | model

def save_conversation_history(history, filename="conversation_history.json"):
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)

# Parse/Load CSV data to json format
def load_json_data(filename):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)

            # Ensure the column headers match expected structure
            df.columns = ['meta_addr', 'name', 'size', 'crtime', 'parent_path']

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
def forward_message_llm(message):
    # Load previous conversation history

    context = ""
    json_data = load_json_data("tempfiles/MOCK_DATA2.csv")  # Initialize JSON data as empty
    print(f"JSON Data: {json_data}")  # Log the JSON data for debugging
  
    # Use Langchain chain to get AI response
    result = chain.invoke({"json_data": json_data ,"question": message})

    # Save new conversation to history
    save_conversation_history()

    return result  # Return the result to be used in Flask

def send_iso(fileName): #vet ej om denna behövs eller kan köras direkt via TSK
    print(fileName)
    return 0

def send_csv(fileName):  #vet ej om denna behövs eller kan köras direkt via OLLAMA
    print(fileName)
    return 0

def is_valid_disk_image(disk_image):
    """
    Checks if a given disk image path is valid by verifying its file extension.
    Returns True if the file extension is valid, False otherwise.
    """
    valid_extensions =[".img",  ".iso", ".vdi", ".vmdk", ".vhd", ".dmg",
                       ".qcow2"] # Add more file types
    _,ext = os.path.splitext(disk_image)
    if ext.lower() not in valid_extensions:
        return False

    return True
