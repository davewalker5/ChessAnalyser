"""
Player database logic
"""

from ..models import Session, Player
from functools import singledispatch
import sqlalchemy as db


def create_player(name, elo, ai):
    """
    Create a new player

    :param name: Player name
    :param elo: Player rating
    :param ai: True if the player is an AI
    :returns: An instance of the Player class for the created record
    """
    with Session.begin() as session:
        player = Player(name=name, elo=elo, ai=ai)
        session.add(player)

    return player


    """
    Return the Player instance for the player with the specified identifier

    :param _: Player name or ID
    :return: Instance of the player
    :raises ValueError: If the player doesn't exist
    """
    raise TypeError("Invalid parameter type")


@singledispatch
def get_player(_):
    """
    Return the Player instance for the player with the specified identifier

    :param _: Player name or ID
    :return: Instance of the player
    """
    raise TypeError("Invalid parameter type")


@get_player.register(str)
def _(name):
    try:
        with Session.begin() as session:
            player = session.query(Player).filter(Player.name == name).one()

    except:
        player = None

    return player


@get_player.register(int)
def _(id):
    with Session.begin() as session:
        player = session.query(Player).get(id)

    return player


def list_players():
    """
    Return a list of players
    """
    with Session.begin() as session:
        query = session.query(Player)
        players = query.order_by(db.asc(Player.name)).all()

    return players
