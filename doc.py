import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def add_to_doc(text):
    # Load credentials from the file
    credentials_path = '/Users/armandhubler/Documents/Python/Tech Lab /ATOS Summary per country/keyfile.json'

    # Check if the file exists
    if not os.path.isfile(credentials_path):
        raise Exception(f'Cannot find service account key file at {credentials_path}')

    # Load credentials from the file
    credentials = service_account.Credentials.from_service_account_file(credentials_path)


    # Connect to the Drive and Docs services
    drive_service = build('drive', 'v3', credentials=credentials)
    docs_service = build('docs', 'v1', credentials=credentials)

    # Create a new blank document
    new_doc = docs_service.documents().create().execute()
    doc_id = new_doc['documentId']

    # Share the document publicly
    drive_service.permissions().create(
        fileId=doc_id,
        body={'role': 'writer', 'type': 'anyone'}
    ).execute()

    # Write the text into the document
    requests = [
        {
            'insertText': {
                'location': {'index': 1},
                'text': text
            }
        }
    ]
    docs_service.documents().batchUpdate(documentId=doc_id,body={'requests': requests}).execute()

    # Return the URL of the new document
    document_url = f"https://docs.google.com/document/d/{doc_id}"
    return document_url


    # streamlit run /Users/franco/PycharmProjects/eg/scratch.py