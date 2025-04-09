from ..constants import OPT_ENGINE, OPT_REFERENCE, OPT_XLSX, OPT_VERBOSE
from ..database.logic import load_analysis, get_analysis_engine_id
from .constants import ANALYSIS_HEADERS, SUMMARY_HEADERS, WIN_CHANCE_HEADERS
from ..analysis.calculations import calculate_win_chance_chart_data, calculate_summary_statistics, extract_player_analysis
from .game_info import load_game_information
from ..utils import check_required_options, WHITE, BLACK, CHECK_FOR_ALL
import xlsxwriter

# Excel Worksheet titles and formatting
INFO_TITLE = "Game Information"
ANALYSIS_TITLE = "Analysis"
WHITE_ANALYSIS_TITLE = "White"
BLACK_ANALYSIS_TITLE = "Black"
SUMMARY_TITLE = "Summary"
WIN_CHANCE_TITLE = "Win Chance"
WIN_CHANCE_CHART_TITLE = "Win Chance Chart"
HEADER_FORMAT = None
CELL_FORMAT = None

def create_workbook(file_path):
    """
    Create a new Excel workbook

    :param file_path: Full path to the workbook to create
    :return: The workbook object
    """
    global HEADER_FORMAT, CELL_FORMAT
    workbook = xlsxwriter.Workbook(file_path)
    HEADER_FORMAT = workbook.add_format({ "bold": True, "align": "left" })
    CELL_FORMAT = workbook.add_format({ "align": "left" })
    return workbook


def save_workbook(workbook):
    """
    Close and save an Excel workbook

    :param workbook: The workbook object to close
    """
    workbook.close()


def add_row_to_worksheet(worksheet, row, data, is_header_row):
    """
    Add a row of data to a worksheet

    :param worksheet: Worksheet object to add the row to
    :param row: Zero-based row index
    :param data: List of values to add, one per column in the row
    :param is_header_row: True if this is the header row
    """
    global HEADER_FORMAT, CELL_FORMAT
    for i, value in enumerate(data):
        if is_header_row:
            worksheet.write(row, i, str(value), HEADER_FORMAT)
        elif isinstance(value, float):
            worksheet.write_number(row, i, round(value, 2), CELL_FORMAT)
        elif isinstance(value, int):
            worksheet.write_number(row, i, value, CELL_FORMAT)
        else:
            worksheet.write(row, i, str(value), CELL_FORMAT)


def create_worksheet(workbook, title, headers, data):
    """
    Create a new worksheet and populate it with column headers and data

    :param workbook: Workbook object to add the worksheet to
    :param title: Title for the new worksheet
    :param headers: List of column headers
    :param data: List of row data lists containing the values
    """

    # Create the worksheet, freeze the first row and hide gridlines
    worksheet = workbook.add_worksheet(title)
    worksheet.freeze_panes(1, 0)
    worksheet.hide_gridlines(2)

    # Add the headers then iterate over the data adding it to each row
    add_row_to_worksheet(worksheet, 0, headers, True)
    for i, row_data in enumerate(data):
        add_row_to_worksheet(worksheet, i + 1, row_data, False)

    # On completion, autofit the worksheet to content
    worksheet.autofit()


def export_analysis_spreadsheet(options):
    """
    Generate an analysis report spreadsheet

    :param options: Dictionary of reporting parameters
    """

    # Check the required options have been supplied
    check_required_options(options, [OPT_ENGINE, OPT_REFERENCE, OPT_XLSX], CHECK_FOR_ALL)

    if options[OPT_VERBOSE]:
        print(f"\nExporting Analysis Report as an Excel Spreadsheet\n")
        print(f"Game reference  : {options[OPT_REFERENCE]}")
        print(f"Analysis engine : {options[OPT_ENGINE]}")
        print(f"XLSX file       : {options[OPT_XLSX]}")
        print("\nLoading analysis results ...")

    # Load the analysis results
    analysis_engine_id = get_analysis_engine_id(options[OPT_ENGINE])
    analysis = load_analysis(options[OPT_REFERENCE], analysis_engine_id)

    # Calculate summary statistics and extract the white and black player analyses from the
    # combined analysis
    if options[OPT_VERBOSE]:
        print("Calculating summary statistics ...")
    summary_statistics = calculate_summary_statistics(analysis)

    if options[OPT_VERBOSE]:
        print("Calculating per-player move analysis ...")
    white_analysis = extract_player_analysis(analysis, WHITE)
    black_analysis = extract_player_analysis(analysis, BLACK)

    # Calculate the win chance chart and table data
    if options[OPT_VERBOSE]:
        print("Generating win chance data ...")
    chart_data = calculate_win_chance_chart_data(analysis)
    chart_table = [[i + 1, x] for i, x in enumerate(chart_data)]

    # Get the game information
    info = load_game_information(options[OPT_REFERENCE], False, options[OPT_ENGINE], True)

    # Create a new Excel workbook to hold the analysis details
    if options[OPT_VERBOSE]:
        print("Creating workbook ...")
    workbook = create_workbook(options[OPT_XLSX])

    # Add the worksheets to the workbook
    create_worksheet(workbook, INFO_TITLE, ["Item", "Value"], info)
    create_worksheet(workbook, SUMMARY_TITLE, SUMMARY_HEADERS, summary_statistics)
    create_worksheet(workbook, WHITE_ANALYSIS_TITLE, ANALYSIS_HEADERS, white_analysis)
    create_worksheet(workbook, BLACK_ANALYSIS_TITLE, ANALYSIS_HEADERS, black_analysis)
    create_worksheet(workbook, ANALYSIS_TITLE, ANALYSIS_HEADERS, analysis)
    create_worksheet(workbook, WIN_CHANCE_TITLE, WIN_CHANCE_HEADERS, chart_table)

    # Add the win chance chart to the workbook
    chart = workbook.add_chart({"type": "area"})
    chart.set_legend({"none": True})

    chart.set_x_axis({
        "major_gridlines": {
            "visible": False
        },
    })

    chart.set_y_axis({
        "min": -100,
        "max": 100,
        "major_gridlines": {
            "visible": True,
            "line": {'width': 1.25, "dash_type": "dash"}
        },
    })

    chart.add_series({
        "values": f"='{WIN_CHANCE_TITLE}'!$B$1:$B${len(chart_data)}"
    })

    worksheet = workbook.add_chartsheet(WIN_CHANCE_CHART_TITLE)
    worksheet.set_chart(chart)

    # Close and save the workbook
    save_workbook(workbook)
