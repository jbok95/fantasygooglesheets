"""Scrapes ESPN box scores and returns all player stats"""
import json
import requests
from bs4 import BeautifulSoup

def get_football_stats(player_stats, url):
    '''
    Scrapes ESPN box scores and returns all player stats

    Parameters:
    - url (str): url location of the ESPN box score

    Returns:
    - filtered_stats (dict): dictionary structured as {name: {stat: stat value}} for all players
    '''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'+
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers, timeout=5)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all script tags, which is where stats JSON is located
    script_tags = soup.find_all('script')

    # Iterate through script tags to find the one containing the target JSON data
    json_data = None
    for script_tag in script_tags:
        if "window['__espnfitt__']" in script_tag.text:
            json_data = json.loads(script_tag.text.split("window['__espnfitt__']=", 1)[1]
                                   .strip(';'))
            break

    if json_data:
        # Extracting the stats data from the JSON structure
        try:
            bxscr_data = json_data['page']['content']['gamepackage']['bxscr']
        except KeyError:
            return None

        for bxscr_item in bxscr_data:
            for stats_data in bxscr_item.get('stats', []):
                for athlt_data in stats_data['athlts']:
                    # Extracting specific information
                    stats_values = athlt_data['stats']

                    # Check if the length of 'stats' is equal to the length of 'keys'
                    if len(stats_values) != len(stats_data['keys']):
                        # Add '0' to 'stats' to match the length of 'keys'
                        stats_values.extend(['0'] * (len(stats_data['keys']) - len(stats_values)))

                    athlete_name = athlt_data['athlt']['dspNm']
                    keys = stats_data['keys']

                    # Create a dictionary for the current athlete
                    athlete_data = dict(zip(keys, stats_values))

                    # Add the athlete data to the player_stats dictionary
                    if athlete_name not in player_stats:
                        player_stats[athlete_name] = {}

                    # Add stats to the athletes
                    for key in keys:
                        player_stats[athlete_name][key] = athlete_data[key]

    # Stats that I want to track
    stat_filter = [
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

    # Filters to exclude all unnecessary stats
    filtered_stats = {
        athlete_name: {
            key: value
            for key, value in athlete_data.items()
            if key in stat_filter
        }
        for athlete_name, athlete_data in player_stats.items()

        # Removes any blank athlete names
        if any(key in stat_filter for key in athlete_data)
    }

    # Return the new filtered stats
    return filtered_stats
