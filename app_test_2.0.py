import json
import os
import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the LLaMA model
model = OllamaLLM(model="llama3.2")

# Create a prompt template
template = """

#Task: Analyze CSV Data 

## Overview
Analyze CSV Data from a disk image and answer questions regarding the contents. 

### CSV File Structure:
The CSV file consists of the following columns:

| Column Name   | Data Type    | Description                                                             |
|---------------|--------------|-------------------------------------------------------------------------|
| **meta_addr** | Integer      | A unique identifier for the file within the database.                  |
| **name**      | String       | The name of the file, including its extension and any suffixes.        |
| **dir_type**  | Integer      | An indicator of the directory type (e.g., 1 for file, 2 for folder).  |
| **size**      | Integer      | The size of the file in bytes.                                         |
| **crtime**    | Integer      | The creation time of the file.                                           |
| **parent_path**| String      | The path to the parent directory where the file is located.            |
| **md5**       | String       | The MD5 hash of the file used for integrity verification.              |

### Example Row:
Below is an example of what a row in the CSV file may look like:
```
303,08df0d2dff81c1bc6770a1a1a68a13[1].png,1,5120,1432644355,/USERS/Jimmy Wilson/AppData/Local/Microsoft/Windows/Temporary Internet Files/Low/Content.IE5/0YNVG0PM/,0d08df0d2dff81c1bc6770a1a1a68a13
```

### Row Breakdown:
Each column in the example row can be interpreted as follows:
- **meta_addr**: `303` - This is the unique identifier for this file.
- **name**: `08df0d2dff81c1bc6770a1a1a68a13[1].png` - The name of the file including its extension.
- **dir_type**: `1` - This indicates that the entry is a file.
- **size**: `5120` - The size of the file is 5120 bytes.
- **crtime**: `1432644355` - This timestamp indicates when the file was created.
- **parent_path**: `/USERS/Jimmy Wilson/AppData/Local/Microsoft/Windows/Temporary Internet Files/Low/Content.IE5/0YNVG0PM/` - This is the path to the directory containing the file.

Answer the question below:

Here is the CSV data: {csv_data}

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Load conversation history from a JSON file
def load_conversation_history(filename="conversation_history.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return an empty dictionary if the file is empty or corrupted
    else:
        # Create the file with an empty JSON object if it doesn't exist
        with open(filename, "w") as file:
            json.dump({}, file)
        return {}

# Save conversation history to a JSON file
def save_conversation_history(history, filename="conversation_history.json"):
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)

# Load CSV data into a string
def load_csv_data(filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        return df.to_string(index=False)  # Return the CSV as a string without row indices
    else:
        print("CSV file does not exist.")
        return ""

# Handle the conversation
def handle_conversation():
    conversation_history = load_conversation_history()
    context = ""
    csv_data = ""  # Initialize CSV data as empty

    # Prompt the user for a CSV file path
    csv_file = input("Enter the path of the CSV file (or leave empty if not using one): ")
    if csv_file:
        csv_data = load_csv_data(csv_file)

    

    print(f"CSV data being sent: {csv_data}")
    
    print("Welcome to chatAI ! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        # Check if the question has been asked before
        if user_input in conversation_history:
            result = conversation_history[user_input]
            print("Old Bot:", result)
        else:
            try:
                result = chain.invoke({"csv_data": csv_data, "question": user_input})
                print("Bot:", result)
            except Exception as e:
                print(f"Error occurred: {str(e)}")
            # Save the new conversation to history
            conversation_history[user_input] = result
        
        context += f"\nUser: {user_input}\nAI: {result}"

    # Save the conversation history when the chat ends
    save_conversation_history(conversation_history)

if __name__ == "__main__":
    handle_conversation()
