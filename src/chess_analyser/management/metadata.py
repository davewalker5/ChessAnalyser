from ..database.logic import load_game, list_metadata_items, create_metadata_value, update_game
from ..database.logic import update_metadata_value as umv


def _update_metadata_value(game, item, value, verbose):
    """
    Update a metadata value

    :param game: Game object
    :param item: Metadata item name
    :param value: Value to set
    :param verbose: True to report actions to the console
    """

    # Load the metadata items and make sure the one of interest is defined
    if verbose:
        print(f"Loading metadata items and validating item '{item}' ...")

    item_name = item.casefold()
    metadata_items = list_metadata_items()
    matching_items = [i for i in metadata_items if i.name.casefold() == item_name]
    if not matching_items:
        raise ValueError(f"Metadata item '{item}' not found")

    # Find the metadata value in the game data. If it's not there, add a new record. If it
    # is, then update the existing one
    if verbose:
        print(f"Locating metadata item '{item}' for game {game.reference} ...")

    game_metadata_items = [i for i in game.meta_data if i.metadata_item_id == matching_items[0].id]
    if not game_metadata_items:
        if verbose:
            print("Creating new metadata item record ...")

        create_metadata_value(metadata_items[0].id, game.id, value)
    else:
        if verbose:
            print("Updating existing metadata item record ...")

        umv(game_metadata_items[0].id, value)


def update_metadata_value(identifier, item, value, verbose):
    """
    Add or update a metadata value

    :param identifier: Game identifier (reference or ID)
    :param item: Metadata item name
    :param value: Value to set
    :param verbose: True to report actions to the console
    """

    if verbose:
        print(f"\nUpdating Game Metadata\n")
        print(f"Game reference  : {identifier}")
        print(f"Metadata Item   : {item}")
        print(f"New value       : {value}")
        print("\nLoading game ...")

    # Load the game
    game = load_game(identifier)
    if not game:
        raise ValueError(f"Game '{identifier}' not found")

    # If the item is the reference, it's stored against the game not as a separate
    # metadata value
    if item.casefold() == "reference":
        update_game(game.id, value, game.white_player_id, game.black_player_id)
    else:
        _update_metadata_value(game, item, value, verbose)
