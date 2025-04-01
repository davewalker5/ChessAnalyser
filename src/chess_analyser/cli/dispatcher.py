import argparse
from ..reporting import tabulate_analysis, tabulate_summary, tabulate_win_chance, \
    write_analysis_spreadsheet, write_analysis_document, tabulate_players
from ..analysis.analysis import analyse_game
from ..constants import PROGRAM_NAME, PROGRAM_DESCRIPTION, PROGRAM_VERSION, OPT_LOAD, OPT_ANALYSE, \
    OPT_RESULTS, OPT_WHITE, OPT_BLACK, OPT_SUMMARY, OPT_WIN_CHANCE, OPT_EXPORT, OPT_PLAYERS, OPT_ENGINE, OPT_PGN, \
    OPT_REFERENCE, OPT_VERBOSE, OPT_XLSX, OPT_DOCX
from ..pgn import import_pgn, export_pgn


def configure_parser():
    """
    Configure the command line parser

    :return: Configured parser object
    """
    parser = argparse.ArgumentParser(
        prog=f"{PROGRAM_NAME} v{PROGRAM_VERSION}",
        description=PROGRAM_DESCRIPTION
    )

    # Main actions
    parser.add_argument("-l", "--load", action="store_true", help="Load a PGN file into the database")
    parser.add_argument("-a", "--analyse", action="store_true", help="Analyse a game using the specified engine")
    parser.add_argument("-r", "--results", action="store_true", help="Print detailed analysis results on the console")
    parser.add_argument("-w", "--white", action="store_true", help="Print detailed analysis results for white on the console")
    parser.add_argument("-b", "--black", action="store_true", help="Print detailed analysis results for black on the console")
    parser.add_argument("-s", "--summary", action="store_true", help="Print an analysis summary on the console")
    parser.add_argument("-wc", "--winchance", action="store_true", help="Print win chance data for an analysis on the console")
    parser.add_argument("-ex", "--export", action="store_true", help="Export analysis results")
    parser.add_argument("-pl", "--players", action="store_true", help="Print a table of players on the console")

    # Values
    parser.add_argument("-p", "--pgn", nargs=1, help="Path to PGN file holding the game to analysis")
    parser.add_argument("-e", "--engine", nargs=1, help="Name of the engine for analysis")
    parser.add_argument("-ref", "--reference", nargs=1, help="Reference for an imported game")
    parser.add_argument("-x", "--xlsx", nargs=1, help="Path to an XLSX file to export to")
    parser.add_argument("-d", "--docx", nargs=1, help="Path to a Word document to export to")

    # Flags
    parser.add_argument("-v", "--verbose", action="store_true", help="Write analysis details to the console during analysis")

    return parser


def parse_command_line():
    """
    Configure the command line parser and parse the command line
    """
    
    # This will automatically generate help if -h or --help is specified and will then exit
    parser = configure_parser()
    args = parser.parse_args()
    
    # Construct a dictionary of options from the command line
    options = {
        # Actions
        OPT_LOAD: args.load,
        OPT_ANALYSE: args.analyse,
        OPT_RESULTS: args.results,
        OPT_WHITE: args.white,
        OPT_BLACK: args.black,
        OPT_SUMMARY: args.summary,
        OPT_WIN_CHANCE: args.winchance,
        OPT_EXPORT: args.export,
        OPT_PLAYERS: args.players,

        # Values
        OPT_ENGINE: args.engine[0] if args.engine else None,
        OPT_PGN: args.pgn[0] if args.pgn else None,
        OPT_REFERENCE: args.reference[0]if args.reference else None,
        OPT_XLSX: args.xlsx[0] if args.xlsx else None,
        OPT_DOCX: args.docx[0] if args.docx else None,

        # Flags
        OPT_VERBOSE: args.verbose
    }

    return options


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


def dispatch_export(options):
    """
    Export the results of an analysis

    :param options: Dictionary of export options
    """

    if options[OPT_XLSX]:
        write_analysis_spreadsheet(options)

    if options[OPT_DOCX]:
        write_analysis_document(options)

    if options[OPT_PGN]:
        export_pgn(options)


def dispatch_command_line(options):
    """
    Dispatch requested command line options

    :param options: Dictionary of options arising from parsing the command line
    """

    try:
        if options[OPT_ANALYSE]:
                analyse_game(options)
        elif options[OPT_LOAD]:
            import_pgn(options)
        elif options[OPT_EXPORT]:
            dispatch_export(options)
        else:
            dispatch_report(options)

    except Exception as e:
        print(str(e))



def handle_command_line():
    """
    Parse the command line and take action based on the specified command line arguments
    """

    options = parse_command_line()
    dispatch_command_line(options)
