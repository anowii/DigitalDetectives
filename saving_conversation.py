import json
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import csv

template = """
Answer the question below:

Here is the conversation history: {context}

Here is the file structure, important to save enerything as this is a copy of a file system: {file}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

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

def save_conversation_history(history, filename="conversation_history.json"):
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)

def saving_test(history, filename="test.json"):
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)

def handle_conversation():
    conversation_history = load_conversation_history()
    context = ""
    if conversation_history:
        for user_input, result in conversation_history.items():
            context += f"\nUser: {user_input}\nAI: {result}"
        chain.invoke({"context": context, "question": user_input})
        context = ""

    print("Welcome to chat with Llama3! Type 'exit' to quit.")
    data = ""
    while True:
        
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        if user_input.lower() == "load":
            with open("tsk/code/proj/db.csv") as file:
                for line in file:
                    data += line + "\n"
            print(data)
        if user_input.lower() == "test":
            with open("test.json") as file:
                context += "The following is a json file that you will need to save as you will need to answer a couple of questions about the data set. You will need to save it as a csv or collection of json atributes of files. "
                for line in file:
                    context += line


        result = chain.invoke({"context": context, "question": user_input, "file":data})
        print("Bot:", result)
        # Save the new conversation to history
        conversation_history[user_input] = result
        context += f"\nUser: {user_input}\nAI: {result}"

    # Save the conversation history when the chat ends
    save_conversation_history(conversation_history)

if __name__ == "__main__":
    handle_conversation()