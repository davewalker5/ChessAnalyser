# Version Information
PROGRAM_NAME = "Chess Analyser"
PROGRAM_DESCRIPTION = "Game analysis using UCI engines"
PROGRAM_VERSION = "1.4.0"

# Members of the analysis options dictionary
OPT_LOAD = "load"
OPT_ANALYSE = "analyse"
OPT_RESULTS = "results"
OPT_WHITE = "white"
OPT_BLACK = "black"
OPT_SUMMARY = "summary"
OPT_WIN_CHANCE = "winchance"
OPT_EXPORT = "export"
OPT_PLAYERS = "players"
OPT_INFO = "info"
OPT_SEARCH = "search"
OPT_DELETE = "delete"

OPT_ENGINE = "engine"
OPT_PGN = "pgn"
OPT_REFERENCE = "reference"
OPT_XLSX = "xlsx"
OPT_DOCX = "docx"

OPT_VERBOSE = "verbose"

# Engine and scoring control
INITIAL_SCORE = 15

# Constants representing the player
WHITE = "White"
BLACK = "Black"

def get_player(halfmove):
    """
    Given a halfmove count, determine which player is to play next

    :halfmove:
    """
    player = WHITE if (halfmove % 2) > 0 else BLACK
    return player
