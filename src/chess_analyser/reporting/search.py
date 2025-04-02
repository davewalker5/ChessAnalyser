from ..database.logic import search_metadata_values, load_games
from .console_reports import tabulate_games


def search_metadata(search_term):
    """
    Search the metadata for games matching a search term and tabulate those games

    :param search_term: Text to look for
    """
    # Search the metadata to get the matching game IDs
    game_ids = search_metadata_values(search_term)

    if game_ids:
        # Load and tabulate the matching games
        games = load_games(game_ids)
        tabulate_games(games)
    else:
        print(f"No games matched the search term '{search_term}")
