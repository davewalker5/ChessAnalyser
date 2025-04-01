from cairosvg import svg2png
import chess.svg
from ..analysis.calculations import calculate_win_chance_chart_data
from ..database.logic import load_game
import matplotlib.pyplot as plt
import os
import pandas as pd


def write_board_position_image(identifier):
    """
    Generate a PNG image of the final state of the board for a game

    :param identifier: Game identifier
    """
    # Load the game
    game = load_game(identifier)
    if not game:
        raise ValueError(f"Game {identifier} not found")

    # Relationship/navigation properties should load the moves
    if not game.moves:
        raise ValueError(f"No moves found for the game with ID {game.id}")

    # Fast forward to the final recorded move of the game
    board = chess.Board()
    for move in game.moves:
        board.push_uci(move.uci)

    # Now create an SVG image from the board in that position and convert to PNG
    image_file_path = f"board-position-{os.getpid()}.png"
    svg_image = chess.svg.board(board=board)
    svg2png(bytestring=svg_image, write_to=image_file_path)
    return image_file_path


def write_win_percent_chart_image(analysis):
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
