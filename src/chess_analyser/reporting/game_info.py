from ..database.logic import list_metadata_items, load_game
from ..engines import load_engine_definitions, get_engine_display_name


def load_game_information(identifier, engine, pgn_only, include_engine_name):
    """
    Load the game meta-data for a specified game
    """
    headers = []

    # Load the metadata item definitions
    meta_data_items = list_metadata_items()

    # Load the game and check it has some metadata
    game = load_game(identifier)
    if game.meta_data:
        # Add the analysis engine to the game information, if required
        if include_engine_name:
            load_engine_definitions()
            engine_display_name = get_engine_display_name(engine)
            headers.append(["Analysis Engine", engine_display_name])

        # Add the remaining meta-data
        for header in game.meta_data:
            item = [i for i in meta_data_items if i.id == header.metadata_item_id][0]
            if item.is_pgn or not pgn_only:
                headers.append([item.name, header.value])

    return headers