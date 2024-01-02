import os
import gspread
from google.oauth2.service_account import Credentials

# Load credentials from JSON key file
creds = Credentials.from_service_account_file(r"C:\Users\Jamie\Downloads\postseasonfantasy-0fa7a5a5bb58.json", scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

# Authorize using the credentials
gc = gspread.authorize(creds)

# Open the Google Sheet by title
sheet = gc.open('2024 Postseason Fantasy').sheet1

# Get values from a range
values = sheet.get_all_values()
print(values)
