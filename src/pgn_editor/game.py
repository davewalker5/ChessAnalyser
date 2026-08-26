"""Chess game state for the PGN editor."""

from collections.abc import Iterable
from dataclasses import dataclass

import chess
import chess.pgn

PGN_METADATA_DEFAULTS = {
    "Event": "Unknown",
    "Site": "?",
    "Date": "????.??.??",
    "Round": "?",
    "White": "?",
    "Black": "?",
    "Result": "*",
}
VALID_RESULTS = frozenset({"1-0", "0-1", "1/2-1/2", "*"})
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
}


@dataclass(frozen=True)
class CapturedMaterial:
    """Describe the pieces and points captured by one player."""

    pieces: tuple[chess.Piece, ...]
    points: int


class MoveRejectedError(ValueError):
    """Raised when a requested move cannot safely be added to the game."""


class FutureMovesError(MoveRejectedError):
    """Raised when adding a move would replace an existing continuation."""


class GameModel:
    """Maintain one standard-position chess game and its current board."""

    def __init__(self, game: chess.pgn.Game | None = None) -> None:
        """
        Initialise a game model.

        :param game: Optional parsed game whose main line should be loaded.
        """
        self._game = game if game is not None else self._new_game()
        self._apply_metadata_defaults()
        self._moves = list(self._game.mainline_moves())
        self._displayed_ply = len(self._moves)
        self._rebuild_board()

    @staticmethod
    def _new_game() -> chess.pgn.Game:
        """
        Create a game with standard seven-tag roster defaults.

        :return: Empty standard-position game.
        """
        game = chess.pgn.Game()
        game.headers.update(PGN_METADATA_DEFAULTS)
        return game

    @property
    def board(self) -> chess.Board:
        """Return a copy of the current board."""
        return self._board.copy()

    @property
    def has_moves(self) -> bool:
        """Return whether the game contains at least one move."""
        return bool(self._moves)

    @property
    def has_resettable_content(self) -> bool:
        """Return whether Clear Game would change moves or metadata."""
        return self.has_moves or dict(self._game.headers) != PGN_METADATA_DEFAULTS

    @property
    def moves(self) -> tuple[chess.Move, ...]:
        """Return the recorded moves as an immutable tuple."""
        return tuple(self._moves)

    @property
    def displayed_ply(self) -> int:
        """Return the number of moves applied to the displayed board."""
        return self._displayed_ply

    @property
    def has_previous_position(self) -> bool:
        """Return whether navigation can move towards the start."""
        return self._displayed_ply > 0

    @property
    def has_next_position(self) -> bool:
        """Return whether navigation can move towards the game end."""
        return self._displayed_ply < len(self._moves)

    @property
    def has_future_moves(self) -> bool:
        """Return whether moves exist after the displayed position."""
        return self.has_next_position

    @property
    def headers(self) -> chess.pgn.Headers:
        """Return a copy of the game's PGN headers."""
        return chess.pgn.Headers(self._game.headers)

    def set_header(self, name: str, value: str) -> bool:
        """
        Update an editable PGN metadata value.

        Blank values are replaced with the field's configured default.

        :param name: Standard PGN metadata field name.
        :param value: New metadata value.
        :return: Whether the stored value changed.
        :raises ValueError: If the field or Result value is unsupported.
        """
        if name not in PGN_METADATA_DEFAULTS:
            raise ValueError(f"Unsupported PGN metadata field: {name}")
        normalised_value = value.strip() or PGN_METADATA_DEFAULTS[name]
        if name == "Result" and normalised_value not in VALID_RESULTS:
            raise ValueError("Result must be 1-0, 0-1, 1/2-1/2 or *")
        if self._game.headers.get(name) == normalised_value:
            return False
        self._game.headers[name] = normalised_value
        return True

    def legal_destinations(self, source: chess.Square) -> frozenset[chess.Square]:
        """
        Return legal destination squares for the piece on a source square.

        Promotion choices that share a destination are represented once.

        :param source: Source square index.
        :return: Legal destination square indices.
        """
        if not chess.SQUARES[0] <= source <= chess.SQUARES[-1]:
            raise ValueError("source must be a valid chess square")
        return frozenset(
            move.to_square
            for move in self._board.legal_moves
            if move.from_square == source
        )

    @property
    def game_over_message(self) -> str | None:
        """Return a concise terminal-position message, if the game is over."""
        if self._board.is_checkmate():
            winner = "Black" if self._board.turn == chess.WHITE else "White"
            return f"Checkmate. {winner} wins."
        if self._board.is_stalemate():
            return "Draw by stalemate."
        outcome = self._board.outcome(claim_draw=False)
        if outcome is not None:
            reason = outcome.termination.name.replace("_", " ").lower()
            return f"Draw by {reason}."
        return None

    def add_move(
        self,
        source: chess.Square,
        destination: chess.Square,
        promotion: chess.PieceType | None = None,
        replace_future: bool = False,
    ) -> str:
        """
        Add a legal move and return its SAN representation.

        :param source: Source square index.
        :param destination: Destination square index.
        :param promotion: Optional promotion piece type.
        :param replace_future: Replace moves after the displayed position.
        :return: Standard algebraic notation for the move.
        :raises MoveRejectedError: If the move cannot safely enter the model.
        :raises FutureMovesError: If confirmation is needed to replace later moves.
        """
        game_over_message = self.game_over_message
        if game_over_message is not None:
            raise MoveRejectedError(game_over_message)
        move = chess.Move(source, destination, promotion=promotion)
        if move not in self._board.legal_moves:
            raise MoveRejectedError("That move cannot be added to the game.")
        if self.has_future_moves and not replace_future:
            raise FutureMovesError("Adding this move will replace later moves.")
        san = self._board.san(move)
        if self.has_future_moves:
            del self._moves[self._displayed_ply :]
        self._moves.append(move)
        self._displayed_ply += 1
        self._board.push(move)
        outcome = self._board.outcome(claim_draw=False)
        if outcome is not None:
            self._game.headers["Result"] = outcome.result()
        self._sync_game()
        return san

    def undo(self) -> bool:
        """Remove the final move, returning whether a move was removed."""
        if not self._moves:
            return False
        final_board = self._game.end().board()
        terminal_move_removed = final_board.outcome(claim_draw=False) is not None
        self._moves.pop()
        self._displayed_ply = len(self._moves)
        self._rebuild_board()
        if terminal_move_removed:
            self._game.headers["Result"] = "*"
        self._sync_game()
        return True

    def clear(self) -> bool:
        """Remove all moves and restore editable metadata defaults."""
        if not self.has_resettable_content:
            return False
        self._game = self._new_game()
        self._moves.clear()
        self._displayed_ply = 0
        self._rebuild_board()
        return True

    def captured_material(self, capturing_color: chess.Color) -> CapturedMaterial:
        """
        Return material captured by one player up to the displayed position.

        :param capturing_color: Colour of the player whose captures are requested.
        :return: Captured pieces and their conventional material-point total.
        """
        board = self._game.board()
        captured_pieces: list[chess.Piece] = []
        for move in self._moves[: self._displayed_ply]:
            moving_color = board.turn
            captured_piece: chess.Piece | None = None
            if board.is_en_passant(move):
                capture_square = move.to_square + (-8 if moving_color else 8)
                captured_piece = board.piece_at(capture_square)
            elif board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
            if moving_color == capturing_color and captured_piece is not None:
                captured_pieces.append(captured_piece)
            board.push(move)
        ordered_pieces = tuple(
            sorted(
                captured_pieces,
                key=lambda piece: (PIECE_VALUES[piece.piece_type], piece.piece_type),
                reverse=True,
            )
        )
        return CapturedMaterial(
            pieces=ordered_pieces,
            points=sum(PIECE_VALUES[piece.piece_type] for piece in ordered_pieces),
        )

    def san_moves(self) -> list[str]:
        """Return SAN text for all moves in order."""
        board = self._game.board()
        result: list[str] = []
        for move in self._moves:
            result.append(board.san(move))
            board.push(move)
        return result

    def navigate_to(self, displayed_ply: int) -> bool:
        """
        Display a position without changing the complete game.

        :param displayed_ply: Number of main-line moves to apply.
        :return: Whether the displayed position changed.
        :raises ValueError: If the ply lies outside the game.
        """
        if not 0 <= displayed_ply <= len(self._moves):
            raise ValueError("displayed_ply must identify a position in the game")
        if displayed_ply == self._displayed_ply:
            return False
        self._displayed_ply = displayed_ply
        self._rebuild_board()
        return True

    def navigate_start(self) -> bool:
        """Display the standard starting position."""
        return self.navigate_to(0)

    def navigate_back(self) -> bool:
        """Display the preceding position, if one exists."""
        if not self.has_previous_position:
            return False
        return self.navigate_to(self._displayed_ply - 1)

    def navigate_forward(self) -> bool:
        """Display the following position, if one exists."""
        if not self.has_next_position:
            return False
        return self.navigate_to(self._displayed_ply + 1)

    def navigate_end(self) -> bool:
        """Display the final game position."""
        return self.navigate_to(len(self._moves))

    def to_pgn(self) -> str:
        """Return a standards-compliant PGN representation."""
        exporter = chess.pgn.StringExporter(
            headers=True, variations=False, comments=False
        )
        return self._game.accept(exporter) + "\n"

    def _rebuild_board(self) -> None:
        """Recreate the current board from the initial position and moves."""
        self._board = self._game.board()
        validation_board = self._game.board()
        try:
            for index, move in enumerate(self._moves):
                if move not in validation_board.legal_moves:
                    raise MoveRejectedError("The game contains an illegal move.")
                validation_board.push(move)
                if index < self._displayed_ply:
                    self._board.push(move)
        except (AssertionError, ValueError) as error:
            raise MoveRejectedError("The game contains an invalid move.") from error

    def _sync_game(self) -> None:
        """Replace the PGN main line with the model's moves."""
        self._game.variations.clear()
        node: chess.pgn.GameNode = self._game
        for move in self._moves:
            node = node.add_main_variation(move)

    def _apply_metadata_defaults(self) -> None:
        """Supply required metadata defaults where values are absent or blank."""
        for name, default_value in PGN_METADATA_DEFAULTS.items():
            current_value = self._game.headers.get(name, "").strip()
            if not current_value or (name == "Event" and current_value == "?"):
                self._game.headers[name] = default_value


def game_from_moves(moves: Iterable[chess.Move]) -> GameModel:
    """
    Build a model from moves, primarily for callers and tests.

    :param moves: Legal moves from the standard starting position.
    :return: Populated game model.
    """
    model = GameModel()
    for move in moves:
        model.add_move(move.from_square, move.to_square, move.promotion)
    return model
