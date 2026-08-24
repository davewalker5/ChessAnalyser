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


def test_save_and_load_preserves_edited_metadata(tmp_path: Path) -> None:
    """All editable metadata should survive a file round trip."""
    model = GameModel()
    expected = {
        "Event": "County Championship",
        "Site": "London",
        "Date": "2026.08.24",
        "Round": "4",
        "White": "Alice",
        "Black": "Bob",
        "Result": "1-0",
    }
    for name, value in expected.items():
        model.set_header(name, value)
    path = tmp_path / "metadata.pgn"
    save_pgn(path, model)

    assert dict(load_pgn(path).model.headers).items() >= expected.items()


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
