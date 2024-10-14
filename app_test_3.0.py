import json
import os
import re
import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

# Define the LLaMA model
model = OllamaLLM(model="phi3:3.8b", num_ctx=4096, temperature=0.5) 


# Create a prompt template
template = """
# Task: Analyze JSON Data

## Overview
You are a knowledgeable forensic assistant capable of answering questions about the provided JSON data from a disk image. 

### JSON File Structure:
The JSON object consists of the following fields:

| Field Name    | Data Type    | Description                                                         |
|---------------|--------------|---------------------------------------------------------------------|
| **meta_addr** | Integer      | A unique identifier for the file within the database.               |
| **name**      | String       | The name of the file, including its extension and any suffixes.     |
| **dir_type**  | Integer      | An indicator of the directory type (e.g., 1 for file, 2 for folder).|
| **size**      | Integer      | The size of the file in bytes.                                      |
| **crtime**    | Integer      | The creation time of the file (Unix timestamp).                     |
| **parent_path**| String      | The path to the parent directory where the file is located.         |
| **md5**       | String       | The MD5 hash of the file, used for integrity verification.          |

### Example JSON Object:
Below is an example of what a JSON object may look like:

```json
{{
  "meta_addr": 303,
  "name": "08df0d2dff81c1bc6770a1a1a68a13[1].png",
  "dir_type": 1,
  "size": 5120,
  "crtime": 1432644355,
  "parent_path": "/USERS/Jimmy Wilson/AppData/Local/Microsoft/Windows/Temporary Internet Files/Low/Content.IE5/0YNVG0PM/",
  "md5": "0d08df0d2dff81c1bc6770a1a1a68a13"
}}```

### JSON Breakdown:
Each column in the example row can be interpreted as follows:
- **meta_addr**: `303` - This is the unique identifier for this file.
- **name**: `08df0d2dff81c1bc6770a1a1a68a13[1].png` - The name of the file, including its extension.
- **dir_type**: `1` - This indicates that the entry is a file (value `1`).
- **size**: `5120` - The size of the file in bytes (5120 bytes).
- **crtime**: `1432644355` - The Unix timestamp indicating when the file was created.
- **parent_path**: `/USERS/Jimmy Wilson/AppData/Local/Microsoft/Windows/Temporary Internet Files/Low/Content.IE5/0YNVG0PM/` - This is the full path to the directory containing the file.
- **md5**: `0d08df0d2dff81c1bc6770a1a1a68a13` - This is the MD5 hash for verifying the file's integrity.

### Required Data for Analysis:
When you analyze the provided CSV data, please refer to the columns as follows:
1. **meta_addr**: Meta address (file identifier).
2. **name**: Filename, including extensions.
3. **dir_type**: Directory type (e.g., 1 for file, 2 for folder).
4. **size**: File size in bytes.
5. **crtime**: File creation timestamp (Unix timestamp).
6. **parent_path**: Directory path containing the file.
7. **md5**: MD5 hash for file integrity.

### Instructions:
You can ask me any question about the JSON data. 
If you ask for specific rows, such as the first or last row, I will provide the complete content.


Here is the conversation history: `{context}`

Here is the JSON data: `{json_data}`

**Question**: {question}

**Answer**: """

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

# Parse/Load CSV data to json format// MÅSTE FIXAS
def load_json_data(filename):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)

            # Ensure the column headers match expected structure
            df.columns = ['meta_addr', 'name', 'dir_type', 'size', 'crtime', 'parent_path', 'md5']

            # Convert to JSON string
            return df.to_dict(orient='records')  # Return the CSV as a string without row indices
        except pd.errors.EmptyDataError:
            print("CSV file is empty or incorrect.")
            return []
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV: {e}")
            return []
    else:
        print("CSV file does not exist.")
        return []

# Handle the conversation
def handle_conversation():
    conversation_history = load_conversation_history()
    context = ""
    json_data = []  # Initialize JSON data as empty

    # Prompt the user for a CSV file path
    csv_file = input("Enter the path of the CSV file (or leave empty if not using one): ")
    if csv_file:
        json_data = load_json_data(csv_file)

        # If the JSON data is empty, skip further processing
        if not json_data:
            print("No valid JSON data loaded. Exiting.")
            return

    # Build context from conversation history_ should be useless for now.
    if conversation_history:
        for user_input, result in conversation_history.items():
            context += f"\nUser: {user_input}\nAI: {result}"

    #Use if you want to check format of json data
    filename = "jsOutput.json"
    with open(filename, 'w', encoding='utf-8') as json_file:
        for entry in json_data:
            json_file.write(json.dumps(entry) + '\n')  


    print("Welcome to chat! Type 'exit' to quit.")
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
                result = chain.invoke({"context": context, "json_data": json_data, "question": user_input})
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
