from ..database.logic import search_metadata_values, load_games
from .console_reports import tabulate_games


def search_metadata(search_terms):
    """
    Search the metadata for games matching a search term and tabulate those games

    :param search_terms: List of terms to look for
    """
    game_ids = None

    # Iterate over the search terms
    for term in search_terms:
        # Search the metadata to get the matching game IDs for this term
        results_for_term = search_metadata_values(term)
        
        # Update the game IDs as the intersection of the current IDs and the results
        # for the current term
        game_ids = results_for_term if not game_ids else game_ids & results_for_term

    if game_ids:
        # Load and tabulate the matching games
        games = load_games(game_ids)
        tabulate_games(games)
    else:
        terms = ", ".join(search_terms)
        print(f"No games matched the search terms '{terms}'")
