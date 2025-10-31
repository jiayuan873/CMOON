import requests 
import json

# Use the keys from the developer portal
access_key = "on_gNeNZYcPBxUUivWs0Y8SY"
secret_key = "ZmSmZs1CkrgRU10LlkAQiPkhfDHi3y9wI2FGhWsR8rR0wuUV"

# Define the header for the request 
headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
           'Content-Type': 'application/json'}

print("=== Fetching Most Recent Document ===")

# First, get the list of documents sorted by modification date
documents_url = "https://cad.onshape.com/api/v10/documents"
documents_params = {
    'sortColumn': 'modifiedAt',
    'sortOrder': 'desc',
    'limit': 1
}

# Get the most recent document
documents_response = requests.get(documents_url, 
                                params=documents_params, 
                                auth=(access_key, secret_key),
                                headers=headers)

if documents_response.status_code == 200:
    documents_data = documents_response.json()
    
    if documents_data.get('items') and len(documents_data['items']) > 0:
        # Get the most recent document
        most_recent_doc = documents_data['items'][0]
        document_id = most_recent_doc['id']
        
        print(f"Most recent document ID: {document_id}")
        print(f"Document name: {most_recent_doc['name']}")
        print(f"Modified at: {most_recent_doc['modifiedAt']}")
        
        print("\n=== Fetching Detailed Document Information ===")
        
        # Now get detailed information about this specific document
        api_url = f"https://cad.onshape.com/api/v10/documents/{document_id}"
        
        # Putting everything together to make the API request 
        response = requests.get(api_url, 
                                auth=(access_key, secret_key),
                                headers=headers)

        # Convert the response to formatted JSON and print the document details
        if response.status_code == 200:
            data = response.json()
            
            print("\n=== DETAILED DOCUMENT INFORMATION ===")
            print(f"Document Name: {data.get('name')}")
            print(f"Document ID: {data.get('id')}")
            print(f"Owner: {data.get('owner', {}).get('name')}")
            print(f"Created At: {data.get('createdAt')}")
            print(f"Modified At: {data.get('modifiedAt')}")
            print(f"Permission: {data.get('permission')}")
            print(f"Public: {data.get('public')}")
            
            # Show workspace information
            if data.get('defaultWorkspace'):
                workspace = data['defaultWorkspace']
                print(f"\nDefault Workspace:")
                print(f"  Name: {workspace.get('name')}")
                print(f"  ID: {workspace.get('id')}")
                print(f"  State: {workspace.get('state')}")
            
            # Show thumbnail if available
            if data.get('thumbnail', {}).get('href'):
                print(f"\nThumbnail: {data['thumbnail']['href']}")
                
            print(f"\nDocument URL: https://cad.onshape.com/documents/{data.get('id')}")
            
            # Optional: Print full JSON for debugging (uncomment if needed)
            # print("\n=== FULL JSON RESPONSE ===")
            # print(json.dumps(data, indent=2))
            
        else:
            print(f"Error fetching document details: {response.status_code}")
            print(response.text)
    else:
        print("No documents found in your account.")
else:
    print(f"Error fetching documents list: {documents_response.status_code}")
    print(documents_response.text)