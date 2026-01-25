import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes required for Blogger
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_credentials(client_secret_file='client_secret.json'):
    """
    Gets valid user credentials from storage.
    If nothing is stored, it logs the user in via browser.
    """
    creds = None
    token_file = 'token.pickle'

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}. Re-authenticating...")
                creds = None

        if not creds:
            if not os.path.exists(client_secret_file):
                print(f"Error: {client_secret_file} not found.")
                print("Please download your OAuth 2.0 Client ID JSON from Google Cloud Console")
                print("and save it as 'client_secret.json' in this directory.")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_blog_id(service):
    """
    Fetches the Blog ID. If multiple, asks user to choose.
    """
    try:
        # Get user's blogs
        blogs = service.blogs().listByUser(userId='self').execute()
        blog_list = blogs.get('items', [])

        if not blog_list:
            print("No blogs found for this account.")
            return None

        if len(blog_list) == 1:
            return blog_list[0]['id']

        print("\nFound multiple blogs:")
        for i, blog in enumerate(blog_list, 1):
            print(f"{i}. {blog['name']} ({blog['url']})")

        choice = input("Select a blog by number: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(blog_list):
                return blog_list[index]['id']
        except ValueError:
            pass

        print("Invalid choice. using first blog.")
        return blog_list[0]['id']

    except Exception as e:
        print(f"Error fetching blogs: {e}")
        return None

def publish_post(title, content, is_draft=False):
    """
    Publishes a post to Blogger.
    """
    creds = get_credentials()
    if not creds:
        return False

    try:
        service = build('blogger', 'v3', credentials=creds)

        # We need a blog ID.
        # For automation, we might want to store it, but for now lets fetch/ask once.
        # Ideally, we cache this too.
        blog_id = None
        if os.path.exists('blog_config.json'):
            with open('blog_config.json', 'r') as f:
                blog_id = json.load(f).get('blog_id')

        if not blog_id:
            blog_id = get_blog_id(service)
            if blog_id:
                with open('blog_config.json', 'w') as f:
                    json.dump({'blog_id': blog_id}, f)

        if not blog_id:
            return False

        body = {
            'title': title,
            'content': content
        }

        posts = service.posts()
        result = posts.insert(blogId=blog_id, body=body, isDraft=is_draft).execute()

        print(f"Successfully published: {result.get('url')}")
        return True

    except Exception as e:
        print(f"An error occurred while publishing: {e}")
        return False

if __name__ == "__main__":
    # Test authentication
    print("Testing Blogger Authentication...")
    creds = get_credentials()
    if creds:
        print("Authentication Successful.")
        service = build('blogger', 'v3', credentials=creds)
        bid = get_blog_id(service)
        print(f"Selected Blog ID: {bid}")
