import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from SQLite.db_handler import DBHandler
from Tools.status_message_builder import StatusMessageBuilder

import Tools.gmail_reader as gmail_reader

SCRIPT_ID = 4

mb = StatusMessageBuilder()

credentials_path = "../Resources/credentials.json"
token_path = "../Resources/token.pickle"
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']


def connect_to_gmail_api():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    gmail_service = build('gmail', 'v1', credentials=creds)
    return gmail_service


def get_messages(gmail_service):
    results = gmail_service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    if not messages: return None;
    return messages



if __name__ == '__main__':
    try:
        db = DBHandler("../SQLite/database.db")
        service = connect_to_gmail_api()
        messages_count = len(get_messages(service))
        old_message_count = db.get_value_from_column_by_id("gmail", "mail_count", "1")
        if messages_count != old_message_count:
            gmail_reader
            db.update_table("gmail", "mail_count", "1", str(messages_count))
        if len(get_messages(service)) != 0:
            # not every mail could be extracted
            pass
        db.close_connection()
        mb.send_status_to_server(script_path=__file__, result=mb.successful,
                                 error_message="", script_id=SCRIPT_ID)
    except Exception as e:
        db.close_connection()
        mb.send_status_to_server(script_path=__file__, result=mb.fail,
                             error_message=str(e), script_id=SCRIPT_ID)
