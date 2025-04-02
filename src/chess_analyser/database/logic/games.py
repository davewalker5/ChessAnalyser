"""
Game database logic
"""

from ..models import Session, Game
from functools import singledispatch
from sqlalchemy.orm import noload


def create_game(reference, white_player_id, black_player_id):
    """
    Create a new game

    :param reference: Unique game reference
    :param white_player_id: White player ID
    :param black_player_id: Black player ID
    :returns: An instance of the Game class for the created record
    """

    with Session.begin() as session:
        game = Game(reference=reference, white_player_id=white_player_id, black_player_id=black_player_id)
        session.add(game)

    return game


@singledispatch
def load_game(_):
    """
    Load the Game instance for the player with the specified identifier

    :param _: Game reference or ID
    :return: Instance of the game, with associated moves and analyses
    """
    raise TypeError("Invalid parameter type")


@load_game.register(str)
def _(reference):
    try:
        with Session.begin() as session:
            game = session.query(Game).filter(Game.reference == reference).one()

    except:
        game = None

    return game


@load_game.register(int)
def _(id):
    with Session.begin() as session:
        game = session.query(Game).get(id)

    return game


def load_games(game_ids):
    """
    Return all the games with IDs in the provided list. Note that while metadata is loaded
    the moves and associated analyses are not

    :param game_ids: List of game IDs
    :return: A list of games matching the specified IDs
    """
    with Session.begin() as session:
        games = session.query(Game).filter(Game.id.in_(game_ids)).options(noload(Game.moves)).all()

    return games
