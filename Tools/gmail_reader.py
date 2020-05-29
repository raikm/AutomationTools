import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Tools.package_tracker_manager import get_couriers, create_tracking


credentials_path = "../credentials.json"
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def connect_to_gmail_api():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    gmail_service = build('gmail', 'v1', credentials=creds)
    return gmail_service


def get_messages(gmail_service):
    results = gmail_service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    msg = results.get('messages', [])
    if not msg:
        print("No messages found.")
        return None;
    else:
        print("Message snippets:")
        return msg;


def get_forwared_message(msg):
    _msg = service.users().messages().get(userId='me', id=msg['id']).execute()

    if _msg.get("payload").get("body").get("data"):
        return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    if _msg.get("payload").get("parts")[0].get("body").get("data"):
        return (base64.urlsafe_b64decode(
            _msg.get("payload").get("parts")[0].get("body").get("data").encode("ASCII")).decode(
            "utf-8"))
    return "error"


def get_sender(msg):
    _msg = msg
    return ""


def get_supplier(sender_name, msg):
    # first check db if sender_name has defined delievery company
    # else extract infos from mailadress
    _msg = msg
    return ""


def get_trackingnumber(msg_body):
    # rules for looking "Sendungsnummer", integer longer than 10 ...
    return ""


def delete_message(msg_id):
    try:
        service.users().messages().delete(userId='me', id=msg_id).execute()
    except:
        pass
    pass


if __name__ == '__main__':
    service = connect_to_gmail_api()
    messages = get_messages(service)
    for message in messages:
        sender = get_sender(message)
        supplier = get_supplier(sender, message)
        content = get_forwared_message(message)
        if content == "error":
            continue

        else:
            couriers = get_couriers()
            print(couriers)
            tracking_number = get_trackingnumber(content)
            result = create_tracking(slug=supplier, tracking_number=tracking_number)
            if result:
                # TODO
                delete_message(123)

