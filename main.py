"""Main driver to update Google Sheets for Postseason Fantasy Football"""
from deploy_functions.projections import get_projections
from deploy_functions.send_to_sheets import update_projections
from deploy_functions.stats import get_football_stats


def main():
    """Drives all functions located in deploy_functions"""
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
    update_projections(player_list, "2024 Postseason Fantasy", "Master Player Pool")

    # Update player stats
    player_stats = {}
    espn_urls = [
        "https://www.espn.com/nfl/boxscore/_/gameId/401547623"
    ]
    # Add stats for each game
    for url in espn_urls:
        get_football_stats(player_stats, url)
    # Write stats to Google Sheet

if __name__ == "__main__":
    main()
