"""Main driver to update Google Sheets for Postseason Fantasy Football"""
from deploy_functions.projections import get_projections
from deploy_functions.send_to_sheets import update_projections, update_stats
from deploy_functions.stats import get_football_stats


def main():
    """Drives all functions located in deploy_functions"""

    # Takes inputs from local drive
    run_projections = True
    workbook = "2024 Postseason Fantasy"
    projections_worksheet = "Master Player Pool"
    espn_urls = [
        "https://www.espn.com/nfl/boxscore/_/gameId/401547623",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547624",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547626",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547627",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547628",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547632",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547633",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547634",
        "https://www.espn.com/nfl/boxscore/_/gameId/401547635"
    ]
    stats_worksheet = "Wild Card Player Stats"

    # Reruns player projections if true
    if run_projections:
        player_list = []
        fantasypros_urls = [
            "https://www.fantasypros.com/nfl/rankings/qb.php",
            "https://www.fantasypros.com/nfl/rankings/half-point-ppr-rb.php",
            "https://www.fantasypros.com/nfl/rankings/half-point-ppr-wr.php",
            "https://www.fantasypros.com/nfl/rankings/half-point-ppr-te.php"
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
    update_stats(filtered_stats, workbook, stats_worksheet)

if __name__ == "__main__":
    main()
