"""
Move database logic
"""

from ..models import Session, Move


def create_move(game_id, halfmove, san, uci):
    """
    Create a new move

    :param game_id: ID of the game the move is associated with
    :param halfmove: Halfmove number
    :param san: SAN for the move
    :param uci: UCI notation for the move
    :returns: An instance of the Move class for the created record
    """

    with Session.begin() as session:
        move = Move(game_id=game_id, halfmove=halfmove, san=san, uci=uci)
        session.add(move)

    return move
