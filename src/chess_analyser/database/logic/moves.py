"""
Move database logic
"""

from ..models import Session, Move, Game


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


def delete_moves(game_id):
    """
    Delete all the move records for a game

    :param game_id: ID of the game to delete moves from
    """

    with Session.begin() as session:
        # Retrieve the game - the navigation/relationship properties will ensure this loads the moves and,
        # with them, their analyses
        game = session.query(Game).get(game_id)

        # Get a list of move IDs
        move_ids = [m.id for m in game.moves]

        # Delete them all
        session.query(Move).filter(Move.id.in_(move_ids)).delete(synchronize_session=False)
