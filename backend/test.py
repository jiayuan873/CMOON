import requests 
import json

# Assemble the URL for the API call 
api_url = "https://cad.onshape.com/api/v10/documents/5c4b4587fdf510d6aec2794e"

# Optional query parameters can be assigned 
params = {}

# Use the keys from the developer portal
access_key = "on_gNeNZYcPBxUUivWs0Y8SY"
secret_key = "ZmSmZs1CkrgRU10LlkAQiPkhfDHi3y9wI2FGhWsR8rR0wuUV"

# Define the header for the request 
headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
           'Content-Type': 'application/json'}

# Putting everything together to make the API request 
response = requests.get(api_url, 
                        params=params, 
                        auth=(access_key, secret_key),
                        headers=headers)
    
# Convert the response to formatted JSON and print the `name` property
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))  # full JSON
    
    # Example: print some key metadata fields
    print("Document Name:", data.get("name"))
    print("Document ID:", data.get("id"))
    print("Owner:", data.get("owner", {}).get("name"))
    print("Created At:", data.get("createdAt"))
else:
    print("Error:", response.status_code)
    print(response.text)