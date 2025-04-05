from ..constants import get_player, WHITE
from ..database.logic import load_game
from ..database.models import get_data_path
from .images import export_current_position_image
import chess
import os
from moviepy import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import tempfile

STARTING_POSITION_IMAGE = "start.png"
CAPTION_BORDER_HEIGHT = 30
FONT_PATH = "OpenSans/OpenSans-SemiBold"
FONT_SIZE = 16


def _create_image_clip_from_position(board, caption, folder, image_name, duration):
    """
    Create an image clip from an image generated from the current board position

    :param board: python-chess board object
    :param caption: Caption for the image
    :param folder: Folder to write the image to
    :param image_name: File name for the image
    :param duration: Duration of the clip in seconds
    """
    # Export the board position as an image
    image_path = str(Path(folder) / Path(image_name))
    _ = export_current_position_image(board, image_path)

    # Load the original image and get its size
    original = Image.open(image_path)
    width, height = original.size

    # Create a new image with a bottom border to accommodate captions and paste the
    # original into it
    new_image = Image.new("RGBA", (width, height + CAPTION_BORDER_HEIGHT), "black")
    new_image.paste(original, (0, 0))

    try:
        # Load a resizeable font
        data_path = get_data_path()
        font_file = str(Path(data_path) / Path(f"fonts/{FONT_PATH}.ttf"))
        font = ImageFont.truetype(font_file, FONT_SIZE)
    except:
        # Fallback to the default font
        font = ImageFont.load_default()

    # Open a drawing object to draw the caption
    draw = ImageDraw.Draw(new_image)

    # Get the bounding box for the caption
    caption_bbox = draw.textbbox((0, 0), caption, font=font)
    caption_width = caption_bbox[2] - caption_bbox[0]
    caption_height = caption_bbox[3] - caption_bbox[1]

    # Use this to calculate its position
    caption_x = (width - caption_width) / 2
    caption_y = height + 2

    # Draw the caption
    draw.text((caption_x, caption_y), caption, font=font, fill=(255, 255, 255, 255))

    # Save the updated image
    new_image.save(image_path)

    # Create the image clip from the updated image
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
        image_clip = _create_image_clip_from_position(board, "", folder, STARTING_POSITION_IMAGE, clip_duration)
        clips = [image_clip]

        # Iterate over the moves, making each one, in turn, and capturing an image of the board
        for i, move in enumerate(game.moves):
            # Capture the SAN and push the UCI move
            san = move.san
            board.push_uci(move.uci)

            # Generate a caption containing the move
            if get_player(i + 1) == WHITE:
                caption = f"{1 + i // 2}. {san}"
                prev_caption = caption
            else:
                caption = f"{prev_caption} {san}"

            # Generate a board image clip
            image_clip = _create_image_clip_from_position(board, caption, folder, f"{i}.png", clip_duration)
            clips.append(image_clip)

        # Combine all clips into the final video
        fps = 1.0 / clip_duration
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(movie_file, fps=fps, codec="libx264")
