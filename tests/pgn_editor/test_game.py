"""Tests for PGN editor game state."""

import chess
import pytest

from pgn_editor.game import FutureMovesError, GameModel, MoveRejectedError


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


def test_navigation_changes_position_without_mutating_game() -> None:
    """Navigating should change only the displayed board and cursor."""
    model = GameModel()
    for source, destination in (("e2", "e4"), ("e7", "e5"), ("g1", "f3")):
        play(model, source, destination)
    original_moves = model.moves
    original_pgn = model.to_pgn()

    assert model.navigate_start()
    assert model.displayed_ply == 0
    assert model.board == chess.Board()
    assert model.moves == original_moves
    assert model.to_pgn() == original_pgn

    assert model.navigate_forward()
    assert model.displayed_ply == 1
    assert model.board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE)
    assert model.navigate_end()
    assert model.displayed_ply == 3
    assert model.moves == original_moves


def test_navigation_boundaries_are_safe() -> None:
    """Navigation should report boundaries and reject out-of-range cursors."""
    model = GameModel()
    assert not model.navigate_start()
    assert not model.navigate_back()
    assert not model.navigate_forward()
    assert not model.navigate_end()
    with pytest.raises(ValueError):
        model.navigate_to(1)


def test_editing_from_history_requires_and_replaces_continuation() -> None:
    """A historical edit should replace future moves only when authorised."""
    model = GameModel()
    for source, destination in (("e2", "e4"), ("e7", "e5"), ("g1", "f3")):
        play(model, source, destination)
    model.navigate_to(1)
    original_moves = model.moves

    with pytest.raises(FutureMovesError):
        play(model, "c7", "c5")
    assert model.moves == original_moves
    assert model.displayed_ply == 1

    san = model.add_move(chess.C7, chess.C5, replace_future=True)
    assert san == "c5"
    assert model.san_moves() == ["e4", "c5"]
    assert model.displayed_ply == 2
    assert not model.has_future_moves


def test_legal_destinations_follow_the_current_position() -> None:
    """Destination hints should include only legal moves for the side to move."""
    model = GameModel()
    assert model.legal_destinations(chess.G1) == frozenset({chess.F3, chess.H3})
    assert model.legal_destinations(chess.G8) == frozenset()

    play(model, "e2", "e4")
    assert model.legal_destinations(chess.E7) == frozenset({chess.E6, chess.E5})
    assert model.legal_destinations(chess.E4) == frozenset()


def test_checkmate_prevents_further_moves_without_changing_state() -> None:
    """A terminal position should reject moves and retain all game state."""
    model = GameModel()
    for source, destination in (
        ("f2", "f3"),
        ("e7", "e5"),
        ("g2", "g4"),
        ("d8", "h4"),
    ):
        play(model, source, destination)
    before_moves = model.moves
    before_board = model.board

    assert model.game_over_message == "Checkmate. Black wins."
    assert model.legal_destinations(chess.E2) == frozenset()
    with pytest.raises(MoveRejectedError, match="Checkmate"):
        play(model, "e2", "e4")
    assert model.moves == before_moves
    assert model.board == before_board
