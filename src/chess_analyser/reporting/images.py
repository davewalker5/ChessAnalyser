from cairosvg import svg2png
import chess
import chess.svg
from ..analysis.calculations import calculate_win_chance_chart_data
from ..database.logic import load_game
from ..utils import check_required_options, CHECK_FOR_ALL
from ..constants import OPT_REFERENCE, OPT_IMAGE, OPT_HALFMOVES, OPT_VERBOSE
import matplotlib.pyplot as plt
import os
import pandas as pd


def fast_forward_game(board, moves, halfmoves):
    """
    Fast forward a game to the point at which a number of halfmoves have been completed

    :param board: Board for the game
    :param moves: Move information
    :param halfmoves: Number of halfmoves to fast-forward
    """
    if halfmoves == "start":
        # A value of "start" for halfmoves means don't fast forward by any moves
        return

    # The halfmove is either "*", for the end of the game, or a number
    target = int(halfmoves) if halfmoves.isdigit() else len(moves)

    # Iterate over the moves, making each one and returning after the specified halfmove has been made
    for i, move in enumerate(moves):
        board.push_uci(move.uci)
        if (i + 1) == target:
            return


def export_current_position_image(board, filename):
    """
    Export a PNG image of the current position of the specified board

    :param board: python-chess board object
    :param filename: Optional filename to export to, or None
    :return: Actual filename written
    """
    image_file_path = filename if filename else f"board-position-{os.getpid()}.png"
    svg_image = chess.svg.board(board=board)
    svg2png(bytestring=svg_image, write_to=image_file_path)
    return image_file_path


def export_board_image_after_halfmoves(identifier, halfmoves, filename, verbose):
    """
    Generate a PNG image of the final state of the board for a game

    :param identifier: Game identifier
    :param halfmoves: Fast-forward by this number of halfmoves before exporting
    :param filename: Optional filename to export to, or None
    :param verbose: True to generate step-by-step output
    :return: Actual filename written
    """

    if verbose:
        print(f"\nExporting Board Image\n")
        print(f"Game reference     : {identifier}")
        print(f"Export at position : {halfmoves} halfmoves")
        print(f"Image file         : {filename}")
        print("\nLoading game ...")

    # Load the game
    game = load_game(identifier)
    if not game:
        raise ValueError(f"Game {identifier} not found")

    # Relationship/navigation properties should load the moves
    if not game.moves:
        raise ValueError(f"No moves found for the game with ID {game.id}")

    # Fast forward to the specified point in the game
    if verbose:
        print(f"Fast-forwarding by {halfmoves} halfmoves ...")

    board = chess.Board()
    fast_forward_game(board, game.moves, halfmoves)

    # Now create an SVG image from the board in that position and convert to PNG
    if verbose:
        print(f"Saving image ...")

    image_file_path = export_current_position_image(board, filename)
    return image_file_path


def export_win_percent_chart_image(analysis):
    """
    Generate a PNG image containing the win percent chart

    :param analysis: Detailed per-move analysis for the whole game
    :return: Image file path
    """

    # Create a data frame holding the chart data
    chart_data = calculate_win_chance_chart_data(analysis)
    df = pd.DataFrame({
        "x": list(range(1, len(chart_data) + 1)),
        "y": chart_data
    })

    # Set the plot size, and axis limits and enable gridlines
    plt.figure(figsize=(6, 2.5))
    axes = plt.gca()
    axes.set_ylim([-100, 100])
    axes.grid(visible=True, which="major", axis="y")

    # Create the area chart
    plt.fill_between(df['x'], df['y'], color='blue', alpha=0.2)
    plt.plot(df['x'], df['y'], color='red', alpha=0.5, linewidth=0.9)

    # Save it as an image file
    image_file_name = f"win-percent-{os.getpid()}.jpg"
    plt.savefig(image_file_name)
    plt.close()

    return image_file_name


def export_board_image(options):
    """
    Export an image of the board

    :param options: Dictionary of export options
    """

    # Check the required options have been supplied
    check_required_options(options, [OPT_REFERENCE, OPT_HALFMOVES, OPT_IMAGE], CHECK_FOR_ALL)

    # Export the image
    export_board_image_after_halfmoves(options[OPT_REFERENCE], options[OPT_HALFMOVES], options[OPT_IMAGE], options[OPT_VERBOSE])
