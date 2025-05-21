import gspread
from google.oauth2.service_account import Credentials
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Google Sheets setup
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "client_secret.json")

creds = Credentials.from_service_account_file(json_path, scopes=scopes)
client = gspread.authorize(creds)

# Open Google Sheet
spreadsheet = client.open("UserData")
sheet = spreadsheet.sheet1

def save_user_data(phone, name, exam):
    try:
        data = [phone, name, exam]
        sheet.append_row(data)
        return "✅ User data saved successfully!"
    except Exception as e:
        return f"⚠️ Error saving data: {str(e)}"

def translate_to_hindi(text):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}
    response = requests.post(
        "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-hi",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()[0]['translation_text']
    return "⚠️ Translation failed."