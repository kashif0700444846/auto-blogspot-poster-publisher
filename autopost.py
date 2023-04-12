import os
import pickle
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Replace this with the path to your OAuth 2.0 client secret JSON file
CLIENT_SECRET_FILE = 'service_account_key.json'

# Replace this with your blog ID
BLOG_ID = '2536051225985325302'

# Replace these with your post title and content
POST_TITLE = 'My Post Title'
POST_CONTENT = 'This is my post content.'

SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_post(blog_id, title, content):
    try:
        creds = get_credentials()
        service = build('blogger', 'v3', credentials=creds)
        body = {
            'title': title,
            'content': content
        }
        result = service.posts().insert(blogId=blog_id, body=body, isDraft=False).execute()
        print(f'Post created with ID {result["id"]}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    create_post(BLOG_ID, POST_TITLE, POST_CONTENT)