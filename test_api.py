import requests
import json

api_url = "https://0fut5yz7b4.execute-api.us-east-1.amazonaws.com/prod"

# Example CSV input string for prediction
test_input = "0.54,22,1,0,1,128,86,159"

payload = {
    "input": test_input
}

response = requests.post(api_url + "/predict", json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
