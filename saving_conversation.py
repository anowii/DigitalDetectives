import json
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the question below:

Here is the conversation history: {context}

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

def handle_conversation():
    conversation_history = load_conversation_history()
    context = ""
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
            result = chain.invoke({"context": context, "question": user_input})
            print("Bot:", result)
            # Save the new conversation to history
            conversation_history[user_input] = result
        
        context += f"\nUser: {user_input}\nAI: {result}"

    # Save the conversation history when the chat ends
    save_conversation_history(conversation_history)

if __name__ == "__main__":
    handle_conversation()