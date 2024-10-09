import requests

url = "http://localhost:4976/forward_message"
message = {
    "message": "This is an external message from Python",
    "external": True
}

response = requests.post(url, json=message)
print(response.json())