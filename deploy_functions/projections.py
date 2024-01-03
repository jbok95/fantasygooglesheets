"""Scrapes fantasypros.com and returns projections for the upcoming week"""
import json
import requests
from bs4 import BeautifulSoup

def get_projections(player_list, url):
    '''
    Scrapes FantasyPros and returns projected player points, appending to the initial list

    Parameters:
    - player_list (list): list of all players including position, team, rank, and proj. score
    - url (str): url location of the ESPN box score

    Returns:
    - player_list (str): same as input but updated for existing data
    '''
    response = requests.get(url, timeout=5)

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
