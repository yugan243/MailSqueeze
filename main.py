import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google.generativeai as genai
import base64
import pickle
import requests

#Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#Gmail Authentication function
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """
    Authenticates and creates a Gmail API service instance.

    Uses OAuth 2.0 credentials from 'tokens.json' if available and valid.
    Otherwise, initiates the OAuth flow to obtain new credentials.

    Returns:
        service: Authorized Gmail API service instance.
    """
    creds = None
    if os.path.exists('tokens.json'):
        creds = Credentials.from_authorized_user_file('tokens.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:  
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                        "project_id": "mailsqueeze-bot", 
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                        "redirect_uris": ["http://localhost"]
                    }
                }, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('tokens.json', 'w') as token:
            token.write(creds.to_json())
            
    service = build('gmail', 'v1', credentials=creds)
    print("Gmail service created successfully.")
    return service

#Function to fetch unread email IDs
def get_unread_emails(service, max_results=5):
    """
    Fetches unread email message IDs from the user's Gmail inbox.

    Args:
        service: Authorized Gmail API service instance.
        max_results: Maximum number of unread messages to fetch (default is 5).

    Returns:
        list of dict: A list of messages, each represented as a dictionary 
                      containing message metadata including the 'id'.
                      Returns an empty list if no unread emails are found.
    """
    results = service.users().messages().list(
        userId='me', 
        labelIds=['INBOX'], 
        q='is:unread', 
        maxResults=max_results
        ).execute()
    return results.get('messages', [])

#Function to extract email content
def get_email_body(service, msg_id):
    """
    Retrieves the plain-text body of an email message by its ID.

    Args:
        service: Authorized Gmail API service instance.
        msg_id: The ID of the email message to retrieve.

    Returns:
        str: The decoded plain-text content of the email body.
             Returns "No readable content found." if no plain-text part is found.
    """
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body']['data']
            text = base64.urlsafe_b64decode(data).decode('utf-8')
            return text
    return "No readable content found."

#Function to mark emails as read
def mark_email_as_read(service, msg_id):
    """
    Marks a Gmail message as read by removing the 'UNREAD' label.
    
    Args:
        service: Authorized Gmail API service instance.
        msg_id: The ID of the Gmail message to mark as read.
    """
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print(f"Email with ID {msg_id} marked as read.")

#Function to summarize the email using gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash')

def summarize_with_gemini(text):
    """
    Summarizes the given text using the Gemini generative AI model.

    Args:
        text: The input string (email body) to summarize.

    Returns:
        str: The summarized text output from the model.
    """
    prompt = f"Summarize this email:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()


#Send the messege to the telegram

def send_to_telegram(message):
    """
    Sends a message to a Telegram chat using a bot.

    Args:
        message: The string message to send to the Telegram chat.

    Returns:
        None
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise error for bad HTTP status
        
        result = response.json()
        if not result.get('ok'):
            print("Telegram API returned an error:", result)
            # You can also raise an exception or log it here
            
        else:
            print("Message sent successfully!")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        # Handle network errors, timeouts, etc.

#Main flow of the program
service = get_gmail_service()
messages = get_unread_emails(service)

if not messages:
    print("No unread emails found.")
else:
    print("Unread emails are summarizing and sending to telegram\n")
    for msg in messages:
        text = get_email_body(service, msg['id'])
        summary = summarize_with_gemini(text)
        send_to_telegram(f"📧 New Email Summary:\n{summary}")
        mark_email_as_read(service, msg['id'])
        print("processed email with ID:", msg['id'])
