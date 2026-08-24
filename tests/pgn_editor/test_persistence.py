"""Tests for transactional PGN persistence."""

from pathlib import Path

import chess
import pytest

from pgn_editor.game import GameModel
from pgn_editor.persistence import PgnFileError, load_pgn, save_pgn


def test_save_and_load_preserves_moves_and_headers(tmp_path: Path) -> None:
    """A saved game should round-trip its main line and standard headers."""
    model = GameModel()
    model.add_move(chess.E2, chess.E4)
    path = tmp_path / "game.pgn"
    save_pgn(path, model)
    loaded = load_pgn(path)
    assert loaded.model.san_moves() == ["e4"]
    assert loaded.model.headers["Result"] == "*"
    assert not loaded.additional_games


def test_multiple_games_are_reported(tmp_path: Path) -> None:
    """Loading should identify PGN text containing another game."""
    path = tmp_path / "games.pgn"
    path.write_text('[Event "One"]\n\n1. e4 *\n\n[Event "Two"]\n\n1. d4 *\n')
    assert load_pgn(path).additional_games


@pytest.mark.parametrize("contents", ["", "1. e5 *"])
def test_invalid_files_are_rejected(tmp_path: Path, contents: str) -> None:
    """Empty and illegal game text should fail without yielding a model."""
    path = tmp_path / "bad.pgn"
    path.write_text(contents)
    with pytest.raises(PgnFileError):
        load_pgn(path)
