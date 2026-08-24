"""Chess game state for the PGN editor."""

from collections.abc import Iterable

import chess
import chess.pgn


class MoveRejectedError(ValueError):
    """Raised when a requested move cannot safely be added to the game."""


class GameModel:
    """Maintain one standard-position chess game and its current board."""

    def __init__(self, game: chess.pgn.Game | None = None) -> None:
        """
        Initialise a game model.

        :param game: Optional parsed game whose main line should be loaded.
        """
        self._game = game if game is not None else self._new_game()
        self._moves = list(self._game.mainline_moves())
        self._rebuild_board()

    @staticmethod
    def _new_game() -> chess.pgn.Game:
        """
        Create a game with standard seven-tag roster defaults.

        :return: Empty standard-position game.
        """
        game = chess.pgn.Game()
        game.headers.update(
            {
                "Event": "?",
                "Site": "?",
                "Date": "????.??.??",
                "Round": "?",
                "White": "?",
                "Black": "?",
                "Result": "*",
            }
        )
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
    def moves(self) -> tuple[chess.Move, ...]:
        """Return the recorded moves as an immutable tuple."""
        return tuple(self._moves)

    @property
    def headers(self) -> chess.pgn.Headers:
        """Return a copy of the game's PGN headers."""
        return chess.pgn.Headers(self._game.headers)

    def add_move(
        self,
        source: chess.Square,
        destination: chess.Square,
        promotion: chess.PieceType | None = None,
    ) -> str:
        """
        Add a legal move and return its SAN representation.

        :param source: Source square index.
        :param destination: Destination square index.
        :param promotion: Optional promotion piece type.
        :return: Standard algebraic notation for the move.
        :raises MoveRejectedError: If the move cannot safely enter the model.
        """
        move = chess.Move(source, destination, promotion=promotion)
        if move not in self._board.legal_moves:
            raise MoveRejectedError("That move cannot be added to the game.")
        san = self._board.san(move)
        self._moves.append(move)
        self._board.push(move)
        self._sync_game()
        return san

    def undo(self) -> bool:
        """Remove the final move, returning whether a move was removed."""
        if not self._moves:
            return False
        self._moves.pop()
        self._rebuild_board()
        self._sync_game()
        return True

    def clear(self) -> bool:
        """Remove all moves while retaining headers."""
        if not self._moves:
            return False
        self._moves.clear()
        self._rebuild_board()
        self._sync_game()
        return True

    def san_moves(self) -> list[str]:
        """Return SAN text for all moves in order."""
        board = self._game.board()
        result: list[str] = []
        for move in self._moves:
            result.append(board.san(move))
            board.push(move)
        return result

    def to_pgn(self) -> str:
        """Return a standards-compliant PGN representation."""
        exporter = chess.pgn.StringExporter(
            headers=True, variations=False, comments=False
        )
        return self._game.accept(exporter) + "\n"

    def _rebuild_board(self) -> None:
        """Recreate the current board from the initial position and moves."""
        self._board = self._game.board()
        try:
            for move in self._moves:
                if move not in self._board.legal_moves:
                    raise MoveRejectedError("The game contains an illegal move.")
                self._board.push(move)
        except (AssertionError, ValueError) as error:
            raise MoveRejectedError("The game contains an invalid move.") from error

    def _sync_game(self) -> None:
        """Replace the PGN main line with the model's moves."""
        self._game.variations.clear()
        node: chess.pgn.GameNode = self._game
        for move in self._moves:
            node = node.add_main_variation(move)


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
