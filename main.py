"""Main driver to update Google Sheets for Postseason Fantasy Football"""
import json
from deploy_functions.projections import get_projections
from deploy_functions.send_to_sheets import update_projections, update_stats
from deploy_functions.stats import get_football_stats


def postseasonfantasy(request):
    """Drives all functions located in deploy_functions"""

    # If request is from local json
    if isinstance(request, str):
        request_json = json.loads(request)

    # If request is from Cloud Scheduler request
    else:
        request_json = request.get_json()

    run_projections = eval(request_json.get('run_projections'))
    workbook = request_json.get('workbook')
    projections_worksheet = request_json.get('projections_worksheet')
    espn_urls = request_json.get('espn_urls')
    stats_worksheet = request_json.get('stats_worksheet')
    start_cell = request_json.get('start_cell')

    # Reruns player projections if true
    if run_projections:
        player_list = []
        fantasypros_urls = [
            "https://www.fantasypros.com/nfl/rankings/qb.php?week=22",
            "https://www.fantasypros.com/nfl/rankings/half-point-ppr-rb.php?week=22",
            "https://www.fantasypros.com/nfl/rankings/half-point-ppr-wr.php?week=22",
            "https://www.fantasypros.com/nfl/rankings/half-point-ppr-te.php?week=22"
        ]
        # Add projections for each position
        for url in fantasypros_urls:
            get_projections(player_list, url)
        # Write projections data to Google Sheet
        update_projections(player_list, workbook, projections_worksheet)

    # Update player stats
    player_stats = {}
    # Add stats for each game
    for url in espn_urls:
        filtered_stats = get_football_stats(player_stats, url)

    # Write stats to Google Sheet
    update_stats(filtered_stats, workbook, stats_worksheet, start_cell)

    return "Success!"

if __name__ == "__main__":
    my_request = {
        "run_projections":"True",
        "workbook":"Postseason Fantasy Stats Master",
        "projections_worksheet":"Master Player Pool",
        "espn_urls":[
            "https://www.espn.com/nfl/boxscore/_/gameId/401547379", #KC/BAL CC
            "https://www.espn.com/nfl/boxscore/_/gameId/401547380" #DET/SF CC
            ],
        "stats_worksheet":"Super Bowl Player Stats",
        "start_cell":"D3"
        }
    my_json = json.dumps(my_request)
    postseasonfantasy(my_json)
