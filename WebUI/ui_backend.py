import json
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate



#TA IN DETTA I EN ANNAN FIL?
template = """
Answer the question below:

Here is the conversation history: {context}

Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


# Helper functions for saving and loading conversation history
def load_conversation_history(filename="conversation_history.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty dictionary if the file is corrupted
    else:
        # Create the file with an empty JSON object if it doesn't exist
        with open(filename, "w") as file:
            json.dump({}, file)
        return {}


def save_conversation_history(history, filename="conversation_history.json"):
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)


# Function to handle message forwarding to LLM
def forward_message_llm(message):
    # Load previous conversation history
    conversation_history = load_conversation_history()
    context = ""

    # Generate context from conversation history
    if conversation_history:
        for user_input, result in conversation_history.items():
            context += f"\nUser: {user_input}\nAI: {result}"

    # Check if the question has been asked before
    if message in conversation_history:
        return conversation_history[message]  # Return cached response

    # Use Langchain chain to get AI response
    result = chain.invoke({"context": context, "question": message})

    # Save new conversation to history
    conversation_history[message] = result
    save_conversation_history(conversation_history)

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



