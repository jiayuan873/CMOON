import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

# ===== CONFIG =====
ACCESS_KEY = "on_gNeNZYcPBxUUivWs0Y8SY"
SECRET_KEY = "ZmSmZs1CkrgRU10LlkAQiPkhfDHi3y9wI2FGhWsR8rR0wuUV"
STEP_FILE_PATH = r"C:\Users\jiayu\Downloads\93332A238_Titanium Helical Insert.STEP"
# ==================

headers = {
    "Accept": "application/json;charset=UTF-8",
    "Content-Type": "application/json;charset=UTF-8"
}

# === STEP 1: Get most recent document ===
doc_response = requests.get(
    "https://cad.onshape.com/api/v10/documents",
    params={"sortColumn": "modifiedAt", "sortOrder": "desc", "limit": 1},
    auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
    headers=headers
)
if doc_response.status_code != 200:
    print("❌ Error fetching documents:", doc_response.text)
    exit()

doc_data = doc_response.json()
if not doc_data.get("items"):
    print("❌ No documents found")
    exit()

document = doc_data["items"][0]
document_id = document["id"]
print(f"✅ Most recent document: {document['name']} ({document_id})")

# === STEP 2: Get default workspace ===
ws_response = requests.get(
    f"https://cad.onshape.com/api/documents/d/{document_id}/workspaces",
    auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
    headers=headers
)
if ws_response.status_code != 200:
    print("❌ Error fetching workspaces:", ws_response.text)
    exit()

ws_data = ws_response.json()
if not ws_data:
    print("❌ No workspaces found in document")
    exit()

workspace_id = ws_data[0]["id"]
print(f"✅ Workspace found: {ws_data[0]['name']} ({workspace_id})")

# === STEP 3: Upload STEP file as blob ===
if not os.path.isfile(STEP_FILE_PATH):
    print(f"❌ STEP file not found: {STEP_FILE_PATH}")
    exit()

with open(STEP_FILE_PATH, "rb") as f:
    files = {'file': (os.path.basename(STEP_FILE_PATH), f)}
    data = {'storeInDocument': 'true', 'formatName': 'STEP'}

    blob_url = f"https://cad.onshape.com/api/v6/blobelements/d/{document_id}/w/{workspace_id}"
    blob_response = requests.post(
        blob_url,
        auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
        files=files,
        data=data
    )

if blob_response.status_code not in [200, 201]:
    print(f"❌ Error uploading STEP file ({blob_response.status_code}): {blob_response.text}")
    exit()

blob_data = blob_response.json()
blob_id = blob_data.get('id')
print("🔍 Blob response:", blob_data)
if not blob_id:
    print("❌ Blob ID not returned by Onshape")
    exit()

print(f"✅ STEP file uploaded successfully! Blob ID: {blob_id}")

# === STEP 4: Import STEP file into new Part Studio ===
time.sleep(5)  # optional delay to ensure blob is ready

import_url = f"https://cad.onshape.com/api/documents/d/{document_id}/w/{workspace_id}/import"
print("🔍 Import URL:", import_url)
import_payload = {
    "format": "STEP",
    "blobElementId": blob_id,
    "flattenAssemblies": False,
    "allowFaultyParts": False
}

import_response = requests.post(
    import_url,
    auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
    headers=headers,
    json=import_payload
)

if import_response.status_code in [200, 201]:
    print("✅ STEP file imported successfully into a new Part Studio!")
    print(import_response.json())
