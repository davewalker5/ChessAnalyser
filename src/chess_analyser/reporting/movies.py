from moviepy import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
from ..database.logic import load_game
from .images import export_current_position_image
import chess
import os
from pathlib import Path
import tempfile

STARTING_POSITION_IMAGE = "start.png"


def _create_image_clip_from_position(board, folder, image_name, duration):
    """
    Create an image clip from an image generated from the current board position

    :param board: python-chess board object
    :param folder: Folder to write the image to
    :param image_name: File name for the image
    :param duration: Duration of the clip in seconds
    """
    # Export the board position as an image
    image_path = str(Path(folder) / Path(image_name))
    _ = export_current_position_image(board, image_path)

    # Create the image clip from the board position
    image_clip = ImageClip(image_path).with_duration(duration)

    # Delete the image
    Path(image_path).resolve().unlink()
    return image_clip


def export_movie(identifier, movie_file, clip_duration):
    """
    Write a movie of all the moves in a game

    :param identifier: Game identifier
    :param movie_file: Output movie file path
    :param clip_duration: Time in seconds between each move
    """

    # Load the game
    game = load_game(identifier)
    if not game:
        raise ValueError(f"Game {identifier} not found")

    # Relationship/navigation properties should load the moves
    if not game.moves:
        raise ValueError(f"No moves found for the game with ID {game.id}")

    # Create a temporary folder to hold the images
    with tempfile.TemporaryDirectory() as folder:
        # Create a board and write the starting position image before any moves
        board = chess.Board()
        image_clip = _create_image_clip_from_position(board, folder, STARTING_POSITION_IMAGE, clip_duration)
        clips = [image_clip]

        # Iterate over the moves, making each one, in turn, and capturing an image of the board
        for i, move in enumerate(game.moves):
            # Capture the SAN and push the UCI move
            san = move.san
            board.push_uci(move.uci)

            # Generate a board image clip
            image_clip = _create_image_clip_from_position(board, folder, f"{i}.png", clip_duration)
            clips.append(image_clip)

        # Combine all clips into the final video
        fps = 1.0 / clip_duration
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(movie_file, fps=fps, codec="libx264")
