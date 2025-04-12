from .parser import parse_command_line
from .export import dispatch_export
from .management import dispatch_delete, dispatch_set_metadata
from .reporting import dispatch_report
from ..reporting import search_metadata
from ..analysis.analysis import analyse_game
from ..constants import PROGRAM_NAME, PROGRAM_DESCRIPTION, PROGRAM_VERSION, OPT_LOAD, OPT_ANALYSE, \
    OPT_EXPORT, OPT_SEARCH, OPT_DELETE, OPT_VERSION, OPT_VERBOSE, OPT_SET
from ..pgn import import_pgn


def dispatch_command_line(options):
    """
    Dispatch requested command line options

    :param options: Dictionary of options arising from parsing the command line
    """

    if options[OPT_VERBOSE] or options[OPT_VERSION]:
        print(f"\n{PROGRAM_NAME} v{PROGRAM_VERSION} - {PROGRAM_DESCRIPTION}")

    try:
        if options[OPT_ANALYSE]:
            analyse_game(options)
        elif options[OPT_LOAD]:
            import_pgn(options)
        elif options[OPT_EXPORT]:
            dispatch_export(options)
        elif options[OPT_SEARCH]:
            search_metadata(options[OPT_SEARCH])
        elif options[OPT_DELETE]:
            dispatch_delete(options)
        elif options[OPT_SET]:
            dispatch_set_metadata(options)
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
