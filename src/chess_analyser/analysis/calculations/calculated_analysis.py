from ...utils import WHITE, BLACK
from ...database.logic import PLAYER_INDEX, CP_LOSS_INDEX, ACCURACY_INDEX, ANNOTATION_INDEX, \
    WIN_PERCENT_INDEX
import statistics


def extract_player_analysis(analysis, player):
    """
    Extract the detailed analysis for one player from the detailed analysis for both

    :param player: Player to extract the analysis for (WHITE or BLACK)
    """
    return [x for x in analysis if x[PLAYER_INDEX] == player]


def calculate_summary_statistics(analysis):
    """
    Given the CP losses and accuracies for each player for a game, calculate their ACPL and
    overall % accuracy then collate and return the summaries for both

    :param analysis: Analysis
    """
    summary_statistics = []
    for player in [WHITE, BLACK]:
        # Extract the analysis for this player
        player_analysis = extract_player_analysis(analysis, player)
        cp_losses = [a[CP_LOSS_INDEX] for a in player_analysis]
        accuracies = [a[ACCURACY_INDEX] for a in player_analysis if a[ACCURACY_INDEX] > 0]
        annotations = [a[ANNOTATION_INDEX] for a in player_analysis if a[ANNOTATION_INDEX]]

        # Calculate the ACPL and overall accuracy
        acpl = statistics.mean(cp_losses)
        accuracy = statistics.harmonic_mean(accuracies)

        # Calculate the counts for each annotation type
        dubious = len([a for a in annotations if a == "?!"])
        mistakes = len([a for a in annotations if a == "?"])
        blunders = len([a for a in annotations if a == "??"])

        summary_statistics.append([
            player,
            acpl,
            accuracy,
            dubious,
            mistakes,
            blunders
        ])

    return summary_statistics


def calculate_win_chance_chart_data(analysis):
    """
    Calculate the data necessary to chart win %

    :param analysis: Complete analysis data for the game
    :return: List of win % chance data points for the chart
    """

    chart_data = []

    # For each iteration, "i" points to the White move analysis and "i + 1" the black
    for i in range(0, len(analysis) - 2, 2):
        black_win_percent = analysis[i + 1][WIN_PERCENT_INDEX]
        if black_win_percent is not None:
            # The chart data is the win % for white - the win % for black
            win_chance = analysis[i][WIN_PERCENT_INDEX] - black_win_percent
            chart_data.append(win_chance)

    return chart_data
