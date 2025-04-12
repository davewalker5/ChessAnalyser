import argparse
from ..constants import PROGRAM_NAME, PROGRAM_DESCRIPTION, PROGRAM_VERSION, OPT_VERSION
from ..constants import OPT_LOAD
from ..constants import OPT_ANALYSE
from ..constants import OPT_RESULTS, OPT_WHITE, OPT_BLACK, OPT_SUMMARY, OPT_WIN_CHANCE, OPT_PLAYERS, OPT_INFO
from ..constants import OPT_EXPORT, OPT_XLSX, OPT_DOCX, OPT_HALFMOVES, OPT_MOVIE, OPT_DURATION
from ..constants import OPT_SEARCH
from ..constants import OPT_DELETE, OPT_SET, OPT_METADATA, OPT_VALUE, OPT_LIST_METADATA
from ..constants import OPT_ENGINE, OPT_PGN, OPT_REFERENCE, OPT_IMAGE, OPT_VERBOSE


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
    parser.add_argument("-ve", "--version", action="store_true", help="Report the application version and exit")
    parser.add_argument("-l", "--load", action="store_true", help="Load a PGN file into the database")
    parser.add_argument("-a", "--analyse", action="store_true", help="Analyse a game using the specified engine")
    parser.add_argument("-r", "--results", action="store_true", help="Print detailed analysis results on the console")
    parser.add_argument("-w", "--white", action="store_true", help="Print detailed analysis results for white on the console")
    parser.add_argument("-b", "--black", action="store_true", help="Print detailed analysis results for black on the console")
    parser.add_argument("-s", "--summary", action="store_true", help="Print an analysis summary on the console")
    parser.add_argument("-wc", "--winchance", action="store_true", help="Print win chance data for an analysis on the console")
    parser.add_argument("-ex", "--export", action="store_true", help="Export analysis results")
    parser.add_argument("-pl", "--players", action="store_true", help="Print a table of players on the console")
    parser.add_argument("-i", "--info", action="store_true", help="Print a table of game information")
    parser.add_argument("-se", "--search", nargs="+", help="Search metadata and print a table of matching games")
    parser.add_argument("-de", "--delete", action="store_true", help="Delete the analysis for a game and engine or all data for a game")
    parser.add_argument("--set", action="store_true", help="Add/update data")
    parser.add_argument("-lm", "--list-metadata", action="store_true", help="List available metadata items")

    # Values
    parser.add_argument("-p", "--pgn", nargs=1, help="Path to PGN file holding the game to analysis")
    parser.add_argument("-e", "--engine", nargs=1, help="Name of the engine for analysis")
    parser.add_argument("-ref", "--reference", nargs=1, help="Reference for an imported game")
    parser.add_argument("-x", "--xlsx", nargs=1, help="Path to an XLSX file to export to")
    parser.add_argument("-d", "--docx", nargs=1, help="Path to a Word document to export to")
    parser.add_argument("-im", "--image", nargs=1, help="Path to an image file (PNG format) to export to")
    parser.add_argument("-hm", "--halfmoves", nargs=1, help="Halfmove number to export an image at")
    parser.add_argument("-mov", "--movie", nargs=1, help="Path to a movie file (MP4 format) to export to")
    parser.add_argument("-du", "--duration", nargs=1, help="Movie frame duration in seconds")
    parser.add_argument("-mi", "--metadata", nargs=1, help="Specify the name of a metadata item to set")
    parser.add_argument("-va", "--value", nargs=1, help="Specify a value to set to set")

    # Flags
    parser.add_argument("-vb", "--verbose", action="store_true", help="Write analysis details to the console during analysis")

    return parser


def get_float_argument_value(value):
    """
    Convert an argument value to a float

    :param value: Argument value
    :return: Floating point number derived from the value or None
    """
    try:
        return float(value[0])

    except:
        return None


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
        OPT_INFO: args.info,
        OPT_SEARCH: args.search,
        OPT_DELETE: args.delete,
        OPT_VERSION: args.version,
        OPT_SET: args.set,
        OPT_LIST_METADATA: args.list_metadata,

        # Values
        OPT_ENGINE: args.engine[0] if args.engine else None,
        OPT_PGN: args.pgn[0] if args.pgn else None,
        OPT_REFERENCE: args.reference[0]if args.reference else None,
        OPT_XLSX: args.xlsx[0] if args.xlsx else None,
        OPT_DOCX: args.docx[0] if args.docx else None,
        OPT_IMAGE: args.image[0] if args.image else None,
        OPT_HALFMOVES: args.halfmoves[0] if args.halfmoves else None,
        OPT_IMAGE: args.image[0] if args.image else None,
        OPT_MOVIE: args.movie[0] if args.movie else None,
        OPT_DURATION: get_float_argument_value(args.duration),
        OPT_METADATA: args.metadata[0] if args.metadata else None,
        OPT_VALUE: args.value[0] if args.value else None,

        # Flags
        OPT_VERBOSE: args.verbose
    }

    return options