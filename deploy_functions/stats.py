import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

def get_football_stats(player_stats, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
            
        # Find all script tags
        script_tags = soup.find_all('script')

        # Iterate through script tags to find the one containing the JSON data
        json_data = None
        for script_tag in script_tags:
            if "window['__espnfitt__']" in script_tag.text:
                json_data = json.loads(script_tag.text.split("window['__espnfitt__']=", 1)[1].strip(';'))
                break

        if json_data:
            # Extracting data from the JSON structure
            bxscr_data = json_data['page']['content']['gamepackage']['bxscr']

            for bxscr_item in bxscr_data:
                for stats_data in bxscr_item.get('stats', []):
                    for athlt_data in stats_data['athlts']:
                        # Extracting desired information
                        stats_values = athlt_data['stats']
                        athlete_name = athlt_data['athlt']['dspNm']
                        keys = stats_data['lbls']

                        # Create a dictionary for the current athlete
                        athlete_data = dict(zip(keys, stats_values))

                        # Add the athlete data to the player_stats dictionary
                        if athlete_name not in player_stats:
                            player_stats[athlete_name] = {}

                        # Add stats to the athletes
                        for key in keys:
                            player_stats[athlete_name][key] = athlete_data[key]

    # Print the new output
    pprint(player_stats)

if __name__ == "__main__":
    player_stats = {}
    url = "https://www.espn.com/nfl/boxscore/_/gameId/401547623"
    get_football_stats(player_stats, url)
