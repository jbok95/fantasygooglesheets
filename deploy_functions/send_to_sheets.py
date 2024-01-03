"""Sends data to Google Sheets"""
import gspread
from google.oauth2.service_account import Credentials

def update_projections(player_list, workbook_title, sheet_title):
    """
    Sends projections to Google Sheets

    Parameters:
    - player_list (list): list of all players including position, team, rank, and proj. score
    - workbook_title (str): name of targeted workbook
    - sheet_title (str): name of targeted sheet

    Returns:
    - None: returns a print success if able to write data
    """
    creds = Credentials.from_service_account_file(r'C:\Users\Jamie\Downloads\postseasonfantasy-0fa7a5a5bb58.json',
                                                  scopes=['https://www.googleapis.com/auth/spreadsheets',
                                                          'https://www.googleapis.com/auth/drive'])
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

    # Write headers
    headers = ["Name", "Team", "Position", "PFPTS", "Rank"]

    # Prepare a list of lists for batch update
    rows_to_update = [headers]

    # Add player information to the list
    for player_info in player_list:
        row_data = [
            player_info['name'],
            player_info['team'],
            player_info['position'],
            player_info['pfpts'],
            player_info['rank']
            ]
        rows_to_update.append(row_data)

    # Batch update the sheet with all rows
    sheet.update('A1', rows_to_update)

def update_stats(player_stats, workbook_title, sheet_title):
    """
    Sends stats to Google Sheets

    Parameters:
    - player_stats (dict): dictionary of all players and relevant fantasy stats
    - workbook_title (str): name of targeted workbook
    - sheet_title (str): name of targeted sheet

    Returns:
    - None: returns a print success if able to write data
    """
    creds = Credentials.from_service_account_file(r'C:\Users\Jamie\Downloads\postseasonfantasy-0fa7a5a5bb58.json',
                                                  scopes=['https://www.googleapis.com/auth/spreadsheets',
                                                          'https://www.googleapis.com/auth/drive'])
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
    headers = [
        'name',
        'passingTouchdowns',
        'passingYards',
        'interceptions',
        'receivingTouchdowns',
        'receivingYards',
        'receptions',
        'rushingTouchdowns',
        'rushingYards',
        'fumblesLost',
        'kickReturnTouchdowns',
        'puntReturnTouchdowns'
    ]
    sheet.append_row(headers)

    # Prepare a list of lists for batch update
    rows_to_update = [headers]

    # Add player information to the list
    for player_name, stats in player_stats.items():
        row_data = [player_name]  # Add player's name to the row data
        for header in headers[1:]:  # Exclude 'name' from headers
            row_data.append(stats.get(header, ''))  # Use get to handle missing keys
        rows_to_update.append(row_data)

    # Batch update the sheet with all rows
    sheet.update('A1', rows_to_update)
