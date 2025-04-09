from .constants import ANALYSIS_HEADERS, SUMMARY_HEADERS, WIN_CHANCE_HEADERS
from .game_info import load_game_information
from ..constants import OPT_ENGINE, OPT_REFERENCE, OPT_WHITE, OPT_BLACK
from ..utils import WHITE, BLACK
from ..database.logic import load_analysis, get_analysis_engine_id, list_players, list_metadata_items
from ..analysis.calculations import calculate_summary_statistics, calculate_win_chance_chart_data, extract_player_analysis

ANALYSIS_COLUMN_WIDTHS = [4, 8, 6, 6, 10, 4, 10, 10, 10, 4, 10, 10]
SUMMARY_COLUMN_WIDTHS = [6, 10, 10, 4, 4, 4]
WIN_CHANCE_COLUMN_WIDTHS = [4, 10]

def _load_analysis(options):
    """
    Load the analysis for the game and engine specified in the options

    :param options: Dictionary of reporting parameters
    """

    analysis_engine_id = get_analysis_engine_id(options[OPT_ENGINE])
    analysis = load_analysis(options[OPT_REFERENCE], analysis_engine_id)
    return analysis


def print_row(values, column_widths):
    """
    Tabulate a set of values as a table row with given column widths. Floating point
    numbers are formatted to 2 decimal places

    :param values: List of alues to tabulate
    :param column_widths: List of integer column widths to pad each column to
    """
    for i, value in enumerate(values):
        if isinstance(value, float):
            value_string = f"{value:.2f}".ljust(column_widths[i])
        else:
            value_string = str(value).ljust(column_widths[i])

        print(f"| {value_string[:column_widths[i]]} ", end='')

    print("|")


def print_separator(column_widths):
    """
    Print the separator between header and table body

    :param column_widths: List of column widths
    """
    row = ["+"]
    for width in column_widths:
        row.append("-" * (2 + width))
        row.append("+")

    print("".join(row))


def tabulate_data(data, headers, column_widths):
    """
    Tabulate a collection of row data lists in the current window

    :param data: List of row data lists to tabulate
    :param headers: List of column headers
    :param column_widths: List of column widths
    """
    print_row(headers, column_widths)
    print_separator(column_widths)
    for row_data in data:
        print_row(row_data, column_widths)


def print_analysis_table_headers():
    """
    Print the headers for the analysis table on the console
    """
    print_row(ANALYSIS_HEADERS, ANALYSIS_COLUMN_WIDTHS)
    print_separator(ANALYSIS_COLUMN_WIDTHS)


def print_analysis_table_row(row_data):
    """
    Print a row of analysis data to the console

    :param row_data: List of values constituting a row of analysis data
    """
    print_row(row_data, ANALYSIS_COLUMN_WIDTHS)


def tabulate_analysis(options):
    """
    Load the analysis for a game and analysis engine, then tabulate it on the console

    :param options: Dictionary of reporting parameters
    """

    # Load the analysis for the game and engine
    analysis = _load_analysis(options)

    # If requested, extract the player-specific analysis
    if options[OPT_WHITE]:
        analysis_to_tabulate = extract_player_analysis(analysis, WHITE)
    elif options[OPT_BLACK]:
        analysis_to_tabulate = extract_player_analysis(analysis, BLACK)
    else:
        analysis_to_tabulate = analysis

    # Print the results
    print_analysis_table_headers()
    for row in analysis_to_tabulate:
        print_analysis_table_row(row)


def tabulate_summary(options):
    """
    Load the analysis for a game and analysis engine, then calculate the analysis summary
    and tabulate it on the console

    :param options: Dictionary of reporting parameters
    """

    # Load the analysis for the game and engine
    analysis = _load_analysis(options)

    # Calculate the summary statistics
    summary_statistics = calculate_summary_statistics(analysis)

    # Print the results
    tabulate_data(summary_statistics, SUMMARY_HEADERS, SUMMARY_COLUMN_WIDTHS)


def tabulate_win_chance(options):
    """
    Load the analysis for a game and analysis engine, then calculate the win chance data
    and tabulate it on the console

    :param options: Dictionary of reporting parameters
    """

    # Load the analysis for the game and engine
    analysis = _load_analysis(options)

    # Use it to calculate the Win Chance data
    win_chance_data = calculate_win_chance_chart_data(analysis)

    # Print the results
    data = [[i, chance] for i, chance in enumerate(win_chance_data)]
    tabulate_data(data, WIN_CHANCE_HEADERS, WIN_CHANCE_COLUMN_WIDTHS)


def tabulate_players():
    """
    Tabulate the current players in the database
    """

    # Get a list of players and convert to tabular data
    players = list_players()
    player_data = [[p.id, p.name[:60], p.elo, p.ai] for p in players]

    # Define the headers
    column_widths = [6, 62, 6, 8]
    headers = ["Id", "Name", "ELO", "AI"]

    # Print the table
    tabulate_data(player_data, headers, column_widths)


def tabulate_game_info(options):
    # Load the game information
    info = load_game_information(options[OPT_REFERENCE], False, None, True)

    # Define the table headers
    column_widths = [20, 60]
    headers = ["Item", "Value"]

    # Print the table
    tabulate_data(info, headers, column_widths)


def tabulate_games(games):
    # Get a list of metadata items so we can pick out the values to tabulate
    items = list_metadata_items()
    item_ids = [
        [i.id for i in items if i.name == "Event"][0],
        [i.id for i in items if i.name == "Date"][0],
        [i.id for i in items if i.name == "White"][0],
        [i.id for i in items if i.name == "Black"][0],
        [i.id for i in items if i.name == "Result"][0]
    ]

    # Extract the data for the table
    data = []
    for game in games:
        # Build the game data for this game, starting with the reference
        game_data = [game.reference]

        # Iterate over the required item IDs
        for i in item_ids:
            # See if this one's set for the game. If it is, extract its value and
            # add it to the game data for this game. Otherwise, just use an empty string
            metadata_value = [v for v in game.meta_data if v.metadata_item_id == i]
            if metadata_value:
                game_data.append(metadata_value[0].value)
            else:
                game_data.append("")

        # Add the data for this game to the table data
        data.append(game_data)

    # Define the column headers
    column_widths = [20, 30, 10, 30, 30, 6]
    headers = ["Reference", "Event", "Date", "White", "Black", "Result"]

    # Tabulate the data
    tabulate_data(data, headers, column_widths)
