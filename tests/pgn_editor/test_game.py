"""Tests for PGN editor game state."""

import chess
import pytest

from pgn_editor.game import GameModel, MoveRejectedError


def play(model: GameModel, source: str, destination: str) -> str:
    """Add one coordinate move to a model."""
    return model.add_move(chess.parse_square(source), chess.parse_square(destination))


def test_moves_generate_san_and_undo() -> None:
    """Moves should produce SAN and undo should restore the prior board."""
    model = GameModel()
    assert play(model, "e2", "e4") == "e4"
    assert play(model, "e7", "e5") == "e5"
    assert play(model, "g1", "f3") == "Nf3"
    assert model.san_moves() == ["e4", "e5", "Nf3"]
    assert model.undo()
    assert model.board.piece_at(chess.G1) == chess.Piece(chess.KNIGHT, chess.WHITE)


def test_illegal_move_does_not_change_state() -> None:
    """A rejected move must not alter history or board state."""
    model = GameModel()
    before = model.board.fen()
    with pytest.raises(MoveRejectedError):
        play(model, "e2", "e5")
    assert model.board.fen() == before
    assert not model.has_moves


def test_castling_and_pgn_export() -> None:
    """Castling should be represented correctly in SAN and PGN."""
    model = GameModel()
    for source, destination in (
        ("e2", "e4"),
        ("e7", "e5"),
        ("g1", "f3"),
        ("b8", "c6"),
        ("f1", "c4"),
        ("g8", "f6"),
    ):
        play(model, source, destination)
    assert play(model, "e1", "g1") == "O-O"
    assert "O-O" in model.to_pgn()


def test_en_passant_and_promotion() -> None:
    """Special pawn moves should update SAN and the board correctly."""
    en_passant_game = GameModel()
    for source, destination in (
        ("e2", "e4"),
        ("a7", "a6"),
        ("e4", "e5"),
        ("d7", "d5"),
    ):
        play(en_passant_game, source, destination)
    assert play(en_passant_game, "e5", "d6") == "exd6"
    assert en_passant_game.board.piece_at(chess.D5) is None

    promotion_game = GameModel()
    for source, destination in (
        ("a2", "a4"),
        ("h7", "h5"),
        ("a4", "a5"),
        ("h5", "h4"),
        ("a5", "a6"),
        ("h4", "h3"),
        ("a6", "b7"),
        ("h3", "g2"),
    ):
        play(promotion_game, source, destination)
    san = promotion_game.add_move(chess.B7, chess.A8, chess.QUEEN)
    assert san.startswith("bxa8=Q")
    assert promotion_game.board.piece_at(chess.A8) == chess.Piece(
        chess.QUEEN, chess.WHITE
    )
