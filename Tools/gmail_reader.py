import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Aftership.package_tracker_manager import get_couriers, create_tracking, update_tracking
from SQLite.db_handler import DBHandler
import re
import aftership
from apiclient import errors
from Tools.status_message_builder import StatusMessageBuilder

SCRIPT_ID = 3

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


def data_encoder(text):
    if len(text)>0:
        message = base64.urlsafe_b64decode(text)
        message = str(message, 'utf-8')
    return message


def get_forwared_message(msg):
    content = service.users().messages().get(userId='me', id=msg['id']).execute()
    if "data" in content['payload']['body']:
        _msg = content['payload']['body']['data']
        return data_encoder(_msg)

    elif "data" in content['payload']['parts'][0]['body']:
        _msg = content['payload']['parts'][0]['body']['data']
        return data_encoder(_msg)
    elif "data" in content['payload']['parts'][0]['parts'][0]['body']:
        _msg = content['payload']['parts'][0]['parts'][0]['body']['data']
        return data_encoder(_msg)
    elif "data" in content['payload']['parts'][0]['parts'][0]['parts'][0]['body']:
        _msg = content['payload']['parts'][0]['parts'][0]['parts'][0]['body']['data']
        return data_encoder(_msg)
    elif "data" in content['payload']['parts']['parts'][0]['parts'][0]['parts'][0][0]['body']:
        _msg = content['payload']['parts'][0]['parts'][0]['parts'][0]['parts'][0]['body']['data']
        return data_encoder(_msg)
    else:
        print("body has no data.")
    return "error"


def get_msg_id(msg):
    try:
        msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        return msg['id']
    except:
        pass


def get_fwd_mail_address(msg):
    _msg = service.users().messages().get(userId='me', id=msg['id']).execute()
    snippet = _msg.get("snippet")
    at_symbol_position = snippet.find("@")

    extracted_string = snippet[at_symbol_position:]
    _list = extracted_string.split()
    return _list[0].lower()


def get_sender(msg):
    mail = get_fwd_mail_address(msg)
    companies = db.get_all_values_from_column("company_supplier", "company")
    for c in companies:
        company = str(c)
        if mail.__contains__(company.lower()):
            return company

    return "N.A."


def get_supplier(sender_name, msg):
    # first check db if sender_name is defined in db
    if sender_name != "N.A.":
        s = db.get_supplier_from_company(sender_name)
        return s
    # no sender mail so check if mail is from supplier itself
    else:
        mail = get_fwd_mail_address(msg)
        mail_domain_list = db.get_all_values_from_column("suppliers", "mail_domain")
        for d in mail_domain_list:
            domain = str(d)
            if mail.__contains__(domain.lower()):
                supplier = db.get_supplier_name(domain)
                return supplier



def get_trackingnumber(company_name, msg_body, supplier):
    if company_name != "N.A.":
        hint = db.get_sender_hint(company_name)
    else:
        try:
            hint = db.get_supplier_hint(supplier)
        except:
            print("TODO ERROR")
            return None
    general_hints = ["Sendnungsnummer", "Trackingnummer", "Sendungsverfolgungsnummer", "trackingnumber", "Paket", "Paketverfolgungsnummern", "AMAZON-Paket"]
    msg_body = msg_body.replace("\n","").replace("\r","")
    if hint:
        result = re.search(hint + r'\s?[A-z, a-z]{0,15}?\s?[:]?\s?[0-9]{3,}', msg_body)
        #result = msg_body.find(hint)

    if result is None:
        for hint in general_hints:
            result = re.search(hint + r'\s?[A-z, a-z]{0,15}?\s?[:]?\s?[0-9]{3,}', msg_body)
            if result is not None:
                break

    start = result.start() + len(hint) + 1
    extracted_string = msg_body[start:start+40].replace(".", "")
    extracted_trackingnumber_string = re.findall(r'\b\d+', extracted_string)
    if len(extracted_trackingnumber_string) > 0 and extracted_trackingnumber_string[0].isdigit():
        try:
            tn = int(extracted_trackingnumber_string[0])
        except:
            #TODO
            print("TODO ERROR")
        if tn is not None:
            return tn
    else:
        return None


def delete_message(msg_id):
    try:
        service.users().messages().delete(userId='me', id=msg_id).execute()
        print('Message with id: %s deleted successfully.' % msg_id)
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    try:
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
                tracking_number = get_trackingnumber(sender, content, supplier)
                if tracking_number is not None and supplier != "N.A.":
                    try:
                        tid = create_tracking(slug=supplier, tracking_number= str(tracking_number))
                        update_tracking(tid, title=str(sender))
                        print(supplier + "     :     " + str(tracking_number))
                        delete_message(get_msg_id(message))
                    except aftership.exception.BadRequest:
                        continue
                elif tracking_number is not None:
                    pass
                    #TODO:
        mb.send_status_to_server(script_path=__file__, result=mb.successful,
                                 error_message="", script_id=SCRIPT_ID)
    except Exception as e:
        db.close_connection()
        mb.send_status_to_server(script_path=__file__, result=mb.fail,
                             error_message=str(e), script_id=SCRIPT_ID)





