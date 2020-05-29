import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Tools.package_tracker_manager import get_couriers, create_tracking
from SQLite.db_handler import DBHandler

credentials_path = "../Resources/credentials.json"
token_path = "../Resources/token.pickle"
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
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
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
        with open(token_path, 'wb') as token:
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
    if _msg.get("payload").get("parts")[0].get("parts")[0].get("body").get("data"):
        return (base64.urlsafe_b64decode(
            _msg.get("payload").get("parts")[0].get("parts")[0].get("body").get("data").encode("ASCII")).decode(
            "utf-8"))
    return "error"


def get_sender(msg):
    messageheader = service.users().messages().get(userId="me", id=msg["id"], format="full", metadataHeaders=None).execute()
    headers = messageheader["payload"]["headers"]
    subject = [i['value'] for i in headers if i["name"] == "Subject"]
    sender = (subject[0])
    # check if in database exists
    # TODO: get sender from first word in Mail
    # check typos
    # else try to get sender from fwd-mail
    return sender


def get_supplier(sender_name, msg):
    # first check db if sender_name is defined in db
    company = check_company_exist(sender_name)
    if company is not None:
        s = db.get_supplier_from_company(company)
        return s
    else:
        #TODO
        # extract infos from mailadress
        _msg = msg
        pass

    return None


def check_company_exist(sender_name):
    companies = db.get_all_values_from_column("company_supplier", "company")
    for c in companies:
        company = str(c)
        if company == sender_name:
            return company
        elif sender_name.__contains__(company):
            return company
        elif company.__contains__(sender_name):
            return company
    return None


def get_trackingnumber(company_name, msg_body):
    hint = db.get_supplier_hint(company_name)
    general_hints = ["Sendnungsnummer", "Trackingnummer", "Sendungsverfolgungsnummer"]

    if hint:
        result = msg_body.find(hint)
    else:
        for hint in general_hints:
            result = msg_body.find(hint)
            if result:
                break
    if result == -1:
        print("nothing found")
    start = result + len(hint) + 1
    extracted_string = msg_body[start:start+40]
    print(extracted_string)
    try:
        tracking_number = [int(s) for s in extracted_string.split() if s.isdigit()]
    except:
        #TODO
        print("TODO ERROR")
    if tracking_number is not None and len(tracking_number) != 0:
        return tracking_number[0]
    else:
        return None


def delete_message(msg_id):
    try:
        service.users().messages().delete(userId='me', id=msg_id).execute()
    except:
        pass
    pass


if __name__ == '__main__':
    couriers = get_couriers()
    db = DBHandler("../SQLite/database.db")
    service = connect_to_gmail_api()
    messages = get_messages(service)


    for message in messages:
        sender = get_sender(message)
        supplier = get_supplier(sender, message)
        content = get_forwared_message(message)
        if content == "error":
            continue
        else:
            tracking_number = get_trackingnumber(sender, content)
            if tracking_number is not None:
                id = create_tracking(slug=supplier, tracking_number= str(tracking_number))
                print ("id=" + id)
                # TODO: add company to infos via aftership method
                #     # TODO
                #     delete_message(123)

            else:
                #TODO
                print("wip")
