"""Transactional PGN file loading and saving."""

import io
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

import chess.pgn

from pgn_editor.game import GameModel, MoveRejectedError


class PgnFileError(Exception):
    """Raised when a PGN file cannot be safely loaded or saved."""


@dataclass(frozen=True)
class LoadedGame:
    """Result of loading the first game from a PGN file."""

    model: GameModel
    additional_games: bool


def load_pgn(path: Path) -> LoadedGame:
    """
    Load and validate the first game from a PGN file.

    :param path: File to read.
    :return: Loaded model and whether another game was present.
    :raises PgnFileError: If no valid first game can be loaded.
    """
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise PgnFileError(f"Could not read {path.name}: {error}") from error
    if not text.strip():
        raise PgnFileError("The selected file is empty.")
    stream = io.StringIO(text)
    try:
        game = chess.pgn.read_game(stream)
    except (ValueError, UnicodeError) as error:
        raise PgnFileError(f"The PGN could not be parsed: {error}") from error
    if game is None:
        raise PgnFileError("The selected file does not contain a chess game.")
    if game.errors:
        raise PgnFileError(f"The PGN contains an invalid move: {game.errors[0]}")
    if "FEN" in game.headers or game.headers.get("SetUp") == "1":
        raise PgnFileError("Games starting from a custom position are not supported.")
    try:
        model = GameModel(game)
    except MoveRejectedError as error:
        raise PgnFileError(str(error)) from error
    try:
        additional_games = chess.pgn.read_game(stream) is not None
    except (ValueError, UnicodeError):
        additional_games = True
    return LoadedGame(model, additional_games)


def save_pgn(path: Path, model: GameModel) -> None:
    """
    Atomically save a game as UTF-8 PGN.

    :param path: Destination path.
    :param model: Game to save.
    :raises PgnFileError: If the game cannot be written.
    """
    temporary_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(model.to_pgn())
            stream.flush()
            os.fsync(stream.fileno())
        temporary_path.replace(path)
    except OSError as error:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise PgnFileError(f"Could not save {path.name}: {error}") from error
