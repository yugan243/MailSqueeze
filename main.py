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
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('tokens.json'):
        creds = Credentials.from_authorized_user_file('tokens.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('tokens.json', 'w') as token:
            token.write(creds.to_json())
            
    service = build('gmail', 'v1', credentials=creds)
    print("Gmail service created successfully.")
    return service

#Function to fetch unread email IDs
def get_unread_emails(service, max_results=5):
    results = service.users().messages().list(
        userId='me', 
        labelIds=['INBOX'], 
        q='is:unread', 
        maxResults=max_results
        ).execute()
    return results.get('messages', [])

#Function to extract email content
def get_email_body(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body']['data']
            text = base64.urlsafe_b64decode(data).decode('utf-8')
            return text
    return "No readable content found."


#Function to summarize the email using gemini-2.5-flash
model = genai.GenerativeModel('models/gemini-2.5-flash')

def summarize_with_gemini(text):
    prompt = f"Summarize this email:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()


#Send the messege to the telegram

def send_to_telegram(message):
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
    for msg in messages:
        text = get_email_body(service, msg['id'])
        summary = summarize_with_gemini(text)
        print("Summary:\n", summary)
        send_to_telegram(f"📧 New Email Summary:\n{summary}")
