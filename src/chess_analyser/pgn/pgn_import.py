from ..database.logic import list_metadata_items, get_player, create_player, load_game, create_game, create_metadata_value, create_move
from ..reporting import tabulate_game_info
from ..utils import check_required_options, CHECK_FOR_ALL
from chess_analyser.constants import OPT_PGN, OPT_REFERENCE, OPT_VERBOSE
import chess
import chess.pgn
from pathlib import Path

# Metadata item names
PGN_FILE_WHITE_PLAYER = "White"
PGN_FILE_BLACK_PLAYER = "Black"
PGN_FILE_PGN = "PGN"
PGN_FEN = "FEN"

# Move dictionary members
HALFMOVE = "halfmove"
SAN = "san"
UCI = "uci"

# Headers dictionary members
HEADERS_ITEM_ID = "metadataitem_id"
HEADERS_VALUE = "value"


def get_pgn_headers(game, metadata_items):
    """
    Retrieve a set of values from a game loaded from a PGN file. The value is the default if the
    value in the PGN is either missing or empty

    :param game: Game object loaded from a PGN file
    :param metadata_items: List of metadata items to get values for
    :return: Dictionary of header values
    """
    headers = {}

    for item in metadata_items:
        value = game.headers.get(item.name,item.default_value).strip()
        if not value:
            value = item.default_value

        headers[item.name] = {
            HEADERS_ITEM_ID: item.id,
            HEADERS_VALUE: value
        }

    return headers


def get_player_id(name):
    """
    Retrieve a named player. If they don't exist, create them with default properties

    :param name: Player name
    :return: Player ID
    """
    player = get_player(name)
    if not player:
        player = create_player(name, 0, False)

    return player.id


def store_game(reference, headers, moves):
    """
    Store a game given the metadata and moves associated with it
    
    :param reference: Unique game reference
    :param headers: PGN metadata headers
    :param moves: List of move dictionaries
    :return: Game ID
    """

    # Check the game doesn't already exist
    game = load_game(reference)
    if game:
        raise ValueError(f"There is an existing game with the reference '{reference}'")

    # Retrieve or create the players
    white_player_id = get_player_id(headers[PGN_FILE_WHITE_PLAYER][HEADERS_VALUE])
    black_player_id = get_player_id(headers[PGN_FILE_BLACK_PLAYER][HEADERS_VALUE])

    # Create the game
    game = create_game(reference, white_player_id, black_player_id)

    # Store the metadata
    for _, properties in headers.items():
        _ = create_metadata_value(properties[HEADERS_ITEM_ID], game.id, properties[HEADERS_VALUE])

    # Create the moves
    for move in moves:
        _ = create_move(game.id, move[HALFMOVE], move[SAN], move[UCI])

    return game.id


def import_pgn(options):
    """
    Import a PGN file into the database

    :param pgn_file_path: Path to the PGN file to import
    :param reference: Unique game reference
    :return: The ID of the imported game
    """
    # Check the required options have been supplied
    check_required_options(options, [OPT_PGN], CHECK_FOR_ALL)

    if options[OPT_VERBOSE]:
        print(f"\nImporting Game from a PGN File\n")
        print(f"PGN File  : {options[OPT_PGN]}")
        print(f"Reference : {options[OPT_REFERENCE]}\n")

    # Check the PGN file exists
    pgn_file = Path(options[OPT_PGN])
    if not pgn_file.is_file():
        raise FileNotFoundError(f"PGN file '{options[OPT_PGN]}' does not exist")

    # Load the PGN file
    with open(options[OPT_PGN], "r") as pgn:
        game = chess.pgn.read_game(pgn)

    #  Extract the standard headers
    if options[OPT_VERBOSE]:
        print("Reading game metadata ...")

    metadata_items = list_metadata_items()
    headers = get_pgn_headers(game, [x for x in metadata_items if x.is_pgn])

    # Add the non-standard headers
    headers[PGN_FILE_PGN] = {
        HEADERS_ITEM_ID: [i.id for i in metadata_items if i.name == PGN_FILE_PGN][0],
        HEADERS_VALUE: pgn_file.name
    }

    # Extract the move data
    if options[OPT_VERBOSE]:
        print("Loading the moves ...")

    moves = []
    board = game.board()
    for i, move in enumerate(game.mainline_moves()):
        # Ignore illegal moves
        if not board.is_legal(move):
            continue

        # Get the SAN and remove any annotations, as these are stored with the analysis not the raw
        # game data
        san = board.san(move)
        san = san.replace("!", "").replace("?", "").strip()

        # Get the UCI notation for the move
        board.push(move)
        uci = str(move)
        moves.append({
            HALFMOVE: i + 1,
            SAN: san,
            UCI: uci
        })

    # Add/overwrite the FEN header with the current board position
    fen = headers[PGN_FEN] = {
        HEADERS_ITEM_ID: [i.id for i in metadata_items if i.name == PGN_FEN][0],
        HEADERS_VALUE: board.fen()
    }

    # Store the game, defaulting the reference to the PGN file name without the extension if no
    # reference is given
    reference = options[OPT_REFERENCE] if options[OPT_REFERENCE] else Path(pgn_file).with_suffix('').stem

    if options[OPT_VERBOSE]:
        print(f"Storing the game with reference {reference} ...\n")

    game_id = store_game(reference, headers, moves)

    # If verbose output's requested, show the game metadata
    if options[OPT_VERBOSE]:
        tabulate_game_info({ OPT_REFERENCE: reference })

    return game_id
