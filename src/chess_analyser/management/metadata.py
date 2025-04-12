from ..database.logic import load_game, list_metadata_items, create_metadata_value, update_game, get_player, create_player
from ..database.logic import update_metadata_value as umv
from ..utils import WHITE, BLACK



def _update_player(game, item, value, verbose):
    """
    Update one of the players in the game record, creating the player if they don't exist

    :param game: Game object
    :param item: Metadata item name
    :param value: Value to set, in this case the player's name
    :param verbose: True to report actions to the console
    """
    # See if the player exists and create them if not
    if verbose:
        print(f"Loading player with name '{value}'")

    player = get_player(value)
    if not player:
        if verbose:
            print(f"Creating new player ...")

        player = create_player(value, 0, False)

    # Apply the player to the game
    if verbose:
        print(f"Setting the {item} player ID to {player.id} ...")

    if item.title() == WHITE:
        update_game(game.id, game.reference, player.id, game.black_player_id)
    else:
        update_game(game.id, game.reference, game.white_player_id, player.id)


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

    # If this is either the white or black player, update the game record
    if item.title() in [WHITE, BLACK]:
        _update_player(game, item, value, verbose)


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
