from ..reporting import export_analysis_spreadsheet, export_analysis_document, export_board_image, \
    export_movie
from ..constants import OPT_PGN, OPT_IMAGE, OPT_XLSX, OPT_DOCX, OPT_MOVIE
from ..pgn import export_pgn


def dispatch_export(options):
    """
    Export the results of an analysis

    :param options: Dictionary of export options
    """

    if options[OPT_XLSX]:
        export_analysis_spreadsheet(options)

    if options[OPT_DOCX]:
        export_analysis_document(options)

    if options[OPT_PGN]:
        export_pgn(options)

    if options[OPT_IMAGE]:
        export_board_image(options)

    if options[OPT_MOVIE]:
        export_movie(options)
