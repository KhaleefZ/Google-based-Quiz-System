import os
import random
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# We need full access to Drive and Forms
SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/gmail.send"
]

# The file you just downloaded
CLIENT_SECRETS_FILE = "credentials.json"
# Where we will save your login "session" so you don't log in every time
TOKEN_FILE = "token.json"

def get_creds():
    creds = None
    # 1. Check if we already have a valid login token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # 2. If no token, or if it expired, let's log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # If refresh fails, force new login
                creds = None
        
        if not creds:
            print("--- LAUNCHING BROWSER FOR LOGIN ---")
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise FileNotFoundError(f"Missing '{CLIENT_SECRETS_FILE}'. Download OAuth Client ID from Google Cloud.")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            # This opens your local browser to sign in
            creds = flow.run_local_server(port=0)
        
        # 3. Save the token for next time
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
            
    return creds

def get_forms_service():
    return build('forms', 'v1', credentials=get_creds())

def get_drive_service():
    return build('drive', 'v3', credentials=get_creds())

def get_gmail_service():
    return build('gmail', 'v1', credentials=get_creds())

def send_email_via_gmail(to_emails: list, subject: str, body_text: str):
    """Sends an email to a list of recipients using Gmail API."""
    import base64
    from email.mime.text import MIMEText

    service = get_gmail_service()

    for recipient in to_emails:
        try:
            # 1. Create the email message
            message = MIMEText(body_text)
            message['to'] = recipient
            message['subject'] = subject

            # 2. Encode it for Gmail (Base64 URL Safe)
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            body = {'raw': raw_message}

            # 3. Send
            service.users().messages().send(userId='me', body=body).execute()
            print(f"✅ Email sent to: {recipient}")

        except Exception as e:
            print(f"❌ Failed to send to {recipient}: {e}")

def delete_google_form(form_id: str):
    """Deletes a file from Google Drive by ID."""
    service = get_drive_service()
    service.files().delete(fileId=form_id).execute()


def create_google_form(title: str, questions: list, shuffle_questions: bool, shuffle_options: bool):
    try:
        # 1. Create the blank form
        forms_service = get_forms_service()
        form_body = {"info": {"title": title, "documentTitle": title}}
        form = forms_service.forms().create(body=form_body).execute()
        form_id = form["formId"]
        form_url = form["responderUri"]

        # --- LOGIC UPDATE: Shuffle Questions Order ---
        if shuffle_questions:
            random.shuffle(questions) 
            # This mixes the order of Question 1, 2, 3...

        # 2. Add Questions
        requests_list = []
        for index, q in enumerate(questions):
            
            # Prepare options list
            options_payload = [{"value": opt} for opt in q.options]

            # Construct the Question Item
            new_question = {
                "createItem": {
                    "item": {
                        "title": q.text,
                        "questionItem": {
                            "question": {
                                "required": True,
                                "grading": {
                                    "pointValue": 1,
                                    "correctAnswers": {
                                        "answers": [{"value": q.correct_answer}]
                                    }
                                },
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": options_payload,
                                    "shuffle": shuffle_options # <--- THIS TELLS GOOGLE TO SHUFFLE OPTIONS
                                }
                            }
                        }
                    },
                    "location": {"index": index}
                }
            }
            requests_list.append(new_question)

        # 3. Batch Update (Send to Google)
        if requests_list:
            forms_service.forms().batchUpdate(
                formId=form_id, 
                body={"requests": requests_list}
            ).execute()

        return {"form_id": form_id, "form_url": form_url}

    except Exception as e:
        print(f"Error creating Google Form: {e}")
        raise e