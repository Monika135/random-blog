# import os
# import google.auth
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload
# from google.oauth2.service_account import Credentials

# SCOPES = ['https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = 'credentials/demoapi-431705-dba0527f4f5d.json'

# PARENT_FOLDER_ID = "1uTCapzTN0QJgzF6Fvgzs3ZAfUNY6cHLE"

# credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# service = build('drive', 'v3', credentials=credentials)

# def upload_image_to_drive(image_file, filename):
#     file_metadata = {
#         'name': filename,
#         'parents': [PARENT_FOLDER_ID],
#         'mimeType': image_file.mimetype
#     }
#     media = MediaIoBaseUpload(image_file, mimetype=image_file.mimetype)
#     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    
#     file_id = file.get('id')
#     permission = {
#         'type': 'anyone',
#         'role': 'reader',
#     }
#     service.permissions().create(fileId=file_id, body=permission).execute()

#     return file_id

# def get_image_url(file_id):
#     return f"https://drive.google.com/uc?id={file_id}"



from dotenv import load_dotenv
import os
import json
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials
# Load environment variables from .env file
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_JSON = os.getenv('SERVICE_ACCOUNT_JSON')
PARENT_FOLDER_ID = os.getenv('PARENT_FOLDER_ID')

credentials_info = json.loads(SERVICE_ACCOUNT_JSON)
credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)

def upload_image_to_drive(image_file, filename):
    file_metadata = {
        'name': filename,
        'parents': [PARENT_FOLDER_ID],
        'mimeType': image_file.mimetype
    }
    media = MediaIoBaseUpload(image_file, mimetype=image_file.mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    file_id = file.get('id')
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file_id, body=permission).execute()

    return file_id

def get_image_url(file_id):
    return f"https://drive.google.com/uc?id={file_id}"
