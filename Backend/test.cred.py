import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define scopes
SCOPES = ["https://www.googleapis.com/auth/drive"]

def check_credentials():
    print("--- 1. CHECKING CREDENTIALS FILE ---")
    if not os.path.exists("credentials.json"):
        print("❌ ERROR: 'credentials.json' not found in this folder.")
        return

    # Load JSON to show which email is being used
    try:
        with open("credentials.json", "r") as f:
            data = json.load(f)
            email = data.get("client_email", "Unknown")
            project = data.get("project_id", "Unknown")
            print(f"✅ File loaded.")
            print(f"   - Project ID: {project}")
            print(f"   - Service Email: {email}")
            print("   (Make sure this matches your NEW service account)")
    except Exception as e:
        print(f"❌ ERROR: Could not read JSON file. {e}")
        return

    print("\n--- 2. CONNECTING TO GOOGLE DRIVE ---")
    try:
        creds = service_account.Credentials.from_service_account_file(
            "credentials.json", scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)
        
        # Check Storage Quota
        about = service.about().get(fields="storageQuota").execute()
        quota = about.get("storageQuota", {})
        limit = int(quota.get("limit", 0))
        usage = int(quota.get("usage", 0))
        
        print(f"✅ Connection Successful!")
        print(f"   - Storage Usage: {usage / (1024*1024):.2f} MB")
        if limit > 0:
            print(f"   - Storage Limit: {limit / (1024*1024):.2f} MB")
        else:
            print("   - Storage Limit: Unlimited (Team Drive/Enterprise)")

    except Exception as e:
        print(f"❌ ERROR: Connection Failed. Reason:\n{e}")
        return

    print("\n--- 3. ATTEMPTING TO CREATE A FILE ---")
    try:
        file_metadata = {'name': 'test_auth.txt'}
        file = service.files().create(body=file_metadata, fields='id').execute()
        print(f"✅ SUCCESS! Created file with ID: {file.get('id')}")
        
        # Cleanup (Delete the test file)
        service.files().delete(fileId=file.get('id')).execute()
        print("   (Test file deleted successfully)")
        
    except Exception as e:
        print(f"❌ ERROR: Could not create file. This confirms the storage/permission issue.")
        print(f"Reason: {e}")

if __name__ == "__main__":
    check_credentials()