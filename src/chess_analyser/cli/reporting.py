from ..reporting import tabulate_analysis, tabulate_summary, tabulate_win_chance, tabulate_players, \
    tabulate_game_info, tabulate_metadata_items
from ..constants import OPT_RESULTS, OPT_WHITE, OPT_BLACK, OPT_SUMMARY, OPT_WIN_CHANCE, OPT_PLAYERS, \
    OPT_INFO, OPT_LIST_METADATA


def dispatch_report(options):
    """
    Generate console-based reports

    :param options: Dictionary of reporting options
    """

    if options[OPT_RESULTS] or options[OPT_WHITE] or options[OPT_BLACK]:
        tabulate_analysis(options)

    if options[OPT_SUMMARY]:
        tabulate_summary(options)

    if options[OPT_WIN_CHANCE]:
        tabulate_win_chance(options)

    if options[OPT_PLAYERS]:
        tabulate_players()

    if options[OPT_INFO]:
        tabulate_game_info(options)

    if options[OPT_LIST_METADATA]:
        tabulate_metadata_items()
