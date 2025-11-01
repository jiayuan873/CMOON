import json
import os
import sys
from onshape_client.client import Client

# Debug information when run from VS Code
print("=== DEBUG INFO ===")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"Script file location: {__file__}")
print(f"Script directory: {os.path.dirname(__file__)}")

# List files in current directory
print("\nFiles in current directory:")
for file in os.listdir("."):
    if file.endswith(('.json', '.py')):
        print(f"  {file}")

# Try to find config.json in multiple locations
config_paths = [
    "config.json",
    os.path.join(os.path.dirname(__file__), "config.json"),
    os.path.join(os.path.dirname(__file__), "..", "config.json"),
]

config_file = None
for path in config_paths:
    if os.path.exists(path):
        config_file = path
        print(f"\n✓ Found config.json at: {path}")
        break

if not config_file:
    print("\n✗ config.json not found in any expected location!")
    print("Searched in:")
    for path in config_paths:
        print(f"  {path}")
    sys.exit(1)

# Load your configuration from the file manually
try:
    with open(config_file) as f:
        config = json.load(f)
    print(f"✓ Config loaded from: {config_file}")
except Exception as e:
    print(f"✗ Error loading config: {e}")
    sys.exit(1)

# Pass the loaded dict to Client()
try:
    client = Client(configuration=config)
    print("✓ Onshape client created successfully")
except Exception as e:
    print(f"✗ Error creating client: {e}")
    sys.exit(1)

# Retrieve the most recently modified document
try:
    print("Fetching documents...")
    docs = client.documents_api.get_documents(sort_column="modifiedAt", sort_order="desc", limit=1)

    if docs.items:
        doc = docs.items[0]
        print("\n=== Most recently modified document ===")
        print(f"Name: {doc.name}")
        print(f"ID: {doc.id}")
        print(f"Modified at: {doc.modified_at}")
        print(f"URL: https://cad.onshape.com/documents/{doc.id}")
    else:
        print("No documents found.")
        
except Exception as e:
    print(f"✗ Error fetching documents: {e}")
    print("This might be due to:")
    print("- Invalid API credentials")
    print("- Network connectivity issues")
    print("- Missing onshape-client library")
    print("Try: pip install onshape-client")