"""Tests for PGN editor game state."""

import chess
import chess.pgn
import pytest

from pgn_editor.game import (
    PGN_METADATA_DEFAULTS,
    FutureMovesError,
    GameModel,
    MoveRejectedError,
)


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
    assert model.headers["Result"] == "0-1"
    assert model.legal_destinations(chess.E2) == frozenset()
    with pytest.raises(MoveRejectedError, match="Checkmate"):
        play(model, "e2", "e4")
    assert model.moves == before_moves
    assert model.board == before_board


def test_undoing_checkmate_restores_unknown_result() -> None:
    """Undoing the terminal move should reset its automatically assigned result."""
    model = GameModel()
    for source, destination in (
        ("f2", "f3"),
        ("e7", "e5"),
        ("g2", "g4"),
        ("d8", "h4"),
    ):
        play(model, source, destination)

    assert model.headers["Result"] == "0-1"
    model.navigate_start()
    assert model.undo()
    assert model.headers["Result"] == "*"


def test_stalemate_sets_draw_result_and_undo_resets_it() -> None:
    """A move causing stalemate should assign and subsequently clear a draw."""
    board = chess.Board("k7/2Q5/2K5/8/8/8/8/8 w - - 0 1")
    model = GameModel(chess.pgn.Game.from_board(board))

    play(model, "c7", "b6")
    assert model.board.is_stalemate()
    assert model.headers["Result"] == "1/2-1/2"

    assert model.undo()
    assert model.headers["Result"] == "*"


def test_metadata_defaults_and_edits_are_exported() -> None:
    """Editable metadata should use defaults and appear in exported PGN."""
    model = GameModel()
    assert (
        dict(model.headers).items()
        >= {
            "Event": "Unknown",
            "Site": "?",
            "Date": "????.??.??",
            "Round": "?",
            "White": "?",
            "Black": "?",
            "Result": "*",
        }.items()
    )

    assert model.set_header("Event", "Club Championship")
    assert model.set_header("White", "Alice")
    assert model.set_header("Site", "   ") is False
    assert '[Event "Club Championship"]' in model.to_pgn()
    assert '[White "Alice"]' in model.to_pgn()


def test_metadata_rejects_unsupported_fields_and_results() -> None:
    """Metadata editing should retain standards-compliant Result values."""
    model = GameModel()
    with pytest.raises(ValueError, match="Unsupported"):
        model.set_header("Opening", "Sicilian")
    with pytest.raises(ValueError, match="Result"):
        model.set_header("Result", "White wins")


def test_captured_material_tracks_both_players_and_navigation() -> None:
    """Captured pieces and totals should describe the displayed position."""
    model = GameModel()
    for source, destination in (
        ("e2", "e4"),
        ("d7", "d5"),
        ("e4", "d5"),
        ("d8", "d5"),
    ):
        play(model, source, destination)

    white = model.captured_material(chess.WHITE)
    black = model.captured_material(chess.BLACK)
    assert white.pieces == (chess.Piece(chess.PAWN, chess.BLACK),)
    assert white.points == 1
    assert black.pieces == (chess.Piece(chess.PAWN, chess.WHITE),)
    assert black.points == 1

    model.navigate_to(2)
    assert model.captured_material(chess.WHITE).points == 0
    assert model.captured_material(chess.BLACK).points == 0


def test_captured_material_handles_en_passant_and_promotion_capture() -> None:
    """Special captures should record the piece removed from its actual square."""
    en_passant_game = GameModel()
    for source, destination in (
        ("e2", "e4"),
        ("a7", "a6"),
        ("e4", "e5"),
        ("d7", "d5"),
        ("e5", "d6"),
    ):
        play(en_passant_game, source, destination)
    en_passant = en_passant_game.captured_material(chess.WHITE)
    assert en_passant.pieces == (chess.Piece(chess.PAWN, chess.BLACK),)
    assert en_passant.points == 1

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
    promotion_game.add_move(chess.B7, chess.A8, chess.QUEEN)
    promotion_capture = promotion_game.captured_material(chess.WHITE)
    assert promotion_capture.pieces == (
        chess.Piece(chess.ROOK, chess.BLACK),
        chess.Piece(chess.PAWN, chess.BLACK),
    )
    assert promotion_capture.points == 6


def test_clear_resets_moves_and_editable_metadata() -> None:
    """Clear should restore a game completely while reporting real changes."""
    model = GameModel()
    assert not model.has_resettable_content
    assert not model.clear()

    model.set_header("White", "Alice")
    assert model.has_resettable_content
    assert model.clear()
    assert dict(model.headers) == PGN_METADATA_DEFAULTS
    assert not model.has_moves
    assert not model.has_resettable_content

    play(model, "e2", "e4")
    assert model.clear()
    assert model.board == chess.Board()
    assert model.displayed_ply == 0

    game_with_extra_metadata = chess.pgn.Game()
    game_with_extra_metadata.headers["Annotator"] = "Example"
    model = GameModel(game_with_extra_metadata)
    assert model.clear()
    assert dict(model.headers) == PGN_METADATA_DEFAULTS
