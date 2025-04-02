from .constants import ANALYSIS_HEADERS, SUMMARY_HEADERS, WIN_CHANCE_HEADERS
from .game_info import load_game_information
from ..constants import OPT_ENGINE, OPT_REFERENCE, OPT_WHITE, OPT_BLACK, WHITE, BLACK
from ..database.logic import load_analysis, get_analysis_engine_id, list_players
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

        print(f"| {value_string} ", end='')

    print("|")


def tabulate_data(data, headers, column_widths):
    """
    Tabulate a collection of row data lists in the current window

    :param data: List of row data lists to tabulate
    :param headers: List of column headers
    :param column_widths: List of column widths
    """
    print()
    print_row(headers, column_widths)
    for row_data in data:
        print_row(row_data, column_widths)


def print_analysis_table_headers():
    """
    Print the headers for the analysis table on the console
    """
    print_row(ANALYSIS_HEADERS, ANALYSIS_COLUMN_WIDTHS)


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
    print_row(SUMMARY_HEADERS, SUMMARY_COLUMN_WIDTHS)
    for row in summary_statistics:
        print_row(row, SUMMARY_COLUMN_WIDTHS)


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
    print_row(WIN_CHANCE_HEADERS, WIN_CHANCE_COLUMN_WIDTHS)
    for i, chance in enumerate(win_chance_data):
        print_row([i + 1, chance], WIN_CHANCE_COLUMN_WIDTHS)


def tabulate_players():
    """
    Tabulate the current players in the database
    """

    # Get a list of players and convert to tabular data
    players = list_players()
    player_data = [[p.id, p.name[:60], p.elo, p.ai] for p in players]

    # Write the headers
    column_widths = [6, 62, 6, 8]
    headers = ["Id", "Name", "ELO", "AI"]
    print_row(headers, column_widths)

    # Write the player data
    for player in player_data:
        print_row(player, column_widths)


def tabulate_game_info(options):
    # Load the game information
    info = load_game_information(options[OPT_REFERENCE], False, None, True)

    # Write the table headers
    column_widths = [20, 60]
    headers = ["Item", "Value"]
    print_row(headers, column_widths)

    # Write the information
    for i in info:
        print_row(i, column_widths)
