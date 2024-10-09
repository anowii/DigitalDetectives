import requests

url = "http://localhost:4980/forward_message"  # Replace with your Flask server address
message = {"message": "This is a message from an external Python script"}

# Send the POST request
response = requests.post(url, json=message)

# Print the response from the server
print(response.json())