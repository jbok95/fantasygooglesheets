import requests
from bs4 import BeautifulSoup
import json
import gspread
from google.oauth2.service_account import Credentials

def get_projections(player_list, url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag containing the player data
        script_tag = soup.find('script', string=lambda x: 'var ecrData' in str(x))

        if script_tag:
            # Extract the JSON data from the script
            script_text = script_tag.text
            json_data = json.loads(script_text.split('var ecrData = ')[1].split(';')[0])

            # Access the "players" list within the JSON data
            players = json_data.get('players', [])

            for player in players:
                name = player.get('player_name', '')
                team = player.get('player_team_id', '')
                position = player.get('player_position_id', '')
                pfpts = player.get('r2p_pts', '')
                rank = player.get('pos_rank', '')

                player_info = {
                    'name': name,
                    'team': team,
                    'position': position,
                    'pfpts': pfpts,
                    'rank': rank
                }

                player_list.append(player_info)

        else:
            print("Script tag not found.")
    else:
        print(f"Error: {response.status_code}")

    return player_list

def write_to_google_sheet(player_list, workbook_title, sheet_title):
    creds = Credentials.from_service_account_file(r'C:\Users\Jamie\Downloads\postseasonfantasy-0fa7a5a5bb58.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    gc = gspread.authorize(creds)

    try:
        # Open the workbook by title
        workbook = gc.open(workbook_title)

        # Try to open the sheet, create if it doesn't exist
        try:
            sheet = workbook.worksheet(sheet_title)
        except gspread.exceptions.WorksheetNotFound:
            sheet = workbook.add_worksheet(title=sheet_title, rows=1, cols=1)

    except gspread.exceptions.SpreadsheetNotFound:
        # Create the workbook if it doesn't exist
        workbook = gc.create(workbook_title)
        sheet = workbook.add_worksheet(title=sheet_title, rows=1, cols=1)

    # Clear existing data in the sheet
    sheet.clear()

    # Write headers
    headers = ["Name", "Team", "Position", "PFPTS", "Rank"]
    sheet.append_row(headers)

    # Prepare a list of lists for batch update
    rows_to_update = [headers]

    # Add player information to the list
    for player_info in player_list:
        row_data = [player_info['name'], player_info['team'], player_info['position'], player_info['pfpts'], player_info['rank']]
        rows_to_update.append(row_data)

    # Batch update the sheet with all rows
    sheet.update('A1', rows_to_update)

    print(f"Data written to Google Sheet: {workbook_title} - {sheet_title}")


if __name__ == "__main__":
    player_list = []

    # Add QB projections
    get_projections(player_list, "https://www.fantasypros.com/nfl/rankings/qb.php")

    # Add RB projections
    get_projections(player_list, "https://www.fantasypros.com/nfl/rankings/half-point-ppr-rb.php")

    # Add WR projections
    get_projections(player_list, "https://www.fantasypros.com/nfl/rankings/half-point-ppr-wr.php")

    # Add TE projections
    get_projections(player_list, "https://www.fantasypros.com/nfl/rankings/half-point-ppr-te.php")

    # Write data to Google Sheet
    write_to_google_sheet(player_list, "2024 Postseason Fantasy", "Master Player Pool")
