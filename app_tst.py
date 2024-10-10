import json
import os
import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the LLaMA model
model = OllamaLLM(model="llama3.1:8b")

# Create a prompt template
template = """
Answer the question below:

Here is the conversation history: {context}

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

    # Build context from conversation history
    if conversation_history:
        for user_input, result in conversation_history.items():
            context += f"\nUser: {user_input}\nAI: {result}"

    print("Welcome to chat with Llama3! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        # Check if the question has been asked before
        if user_input in conversation_history:
            result = conversation_history[user_input]
            print("Bot:", result)
        else:
            result = chain.invoke({"context": context, "csv_data": csv_data, "question": user_input})
            print("Bot:", result)
            # Save the new conversation to history
            conversation_history[user_input] = result
        
        context += f"\nUser: {user_input}\nAI: {result}"

    # Save the conversation history when the chat ends
    save_conversation_history(conversation_history)

if __name__ == "__main__":
    handle_conversation()
