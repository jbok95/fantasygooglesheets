from deploy_functions.projections import get_projections, write_to_google_sheet
from deploy_functions.stats import get_football_stats


def main(request):
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

    # Update player stats
    player_stats = {}
    url = "https://www.espn.com/nfl/boxscore/_/gameId/401547623"
    get_football_stats(player_stats, url)

if __name__ == "__main__":
    main(0)
