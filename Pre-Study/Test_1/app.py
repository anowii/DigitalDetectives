import json
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

OLLAMA_API_URL = 'http://localhost:11434/api/generate'  # Default API endpoint for Ollama running locally
MODEL_NAME = 'llama3.1'  # You can specify the actual LLaMA 3 model name if different

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['question']
    
    # Prepare payload for Ollama API
    payload = {
        "model": MODEL_NAME,
        "prompt": user_input
    }

    # Send the request to Ollama's API
    try:
        # Correct the request by directly passing the payload
        response = requests.post(OLLAMA_API_URL, json=payload, headers={'Content-Type': 'application/json'})
        
        print("Raw response:", response.text)

        response_lines = response.text.strip().splitlines()
        final_response = ""

        # Check if the request was successful
        if response.status_code == 200:
            for line in response_lines:
                try:
                    response_data = json.loads(line)
                    final_response += response_data.get('response','')
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {line}")

            # Safely get the 'text' field from the response, with fallback in case it's missing
            answer = final_response if final_response else "No response text found"
        else:
            answer = f"Error: Received status code {response.status_code} from Ollama API"

    except Exception as e:
        answer = f"Error: {str(e)}"

    # Pass the LLM response back to the UI
    return render_template('indexa.html', question=user_input, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)