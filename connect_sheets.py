import os
import gspread
from google.oauth2.service_account import Credentials

# Define authentication scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(json_path, scopes=scopes)
client = gspread.authorize(creds)

# Get the correct path to client_secret.json
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "client_secret.json")

# Load credentials from JSON file
creds = Credentials.from_service_account_file(json_path, scopes=scopes)
client = gspread.authorize(creds)

# Open Google Sheet
spreadsheet = client.open("UserData")  # Ensure this matches your Google Sheet name
sheet = spreadsheet.sheet1  # ✅ Fixed line

# Function to save user data
def save_user_data(phone, name, exam):
    """Save user data to Google Sheets."""
    try:
        data = [phone, name, exam]
        sheet.append_row(data)  # Append data to the next available row
        return "✅ User data saved successfully!"
    except Exception as e:
        return f"⚠️ Error saving data: {str(e)}"
