"""
Metadata value database logic
"""

from ..models import Session, MetaDataValue, Game


def create_metadata_value(metadata_item_id, game_id, value):
    """
    Create a new player

    :param metadata_item_id: ID for the metadata item of which the value is an instance
    :param game_id: ID of the game that the metadata is associated with
    :param value: Value to add
    :returns: An instance of the MetaDataValue class for the created record
    """

    with Session.begin() as session:
        metadata_value = MetaDataValue(game_id=game_id, metadata_item_id=metadata_item_id, value=value)
        session.add(metadata_value)

    return metadata_value


def update_metadata_value(metadata_value_id, value):
    """
    Update a metadata value

    :param metadata_value_id: ID for the metadata value record to update
    :param value: Value to set
    """
    with Session.begin() as session:
        match = session.query(MetaDataValue).filter(MetaDataValue.id == metadata_value_id).one()
        match.value = value


def search_metadata_values(search_term):
    """
    Search the metadata for values matching the specified search term and return
    the IDs for the parent games

    :param search_term: Text to look for
    :return: Set of matching game IDs
    """
    with Session.begin() as session:
        match_string = f"%{search_term}%"
        matches = session.query(MetaDataValue).filter(MetaDataValue.value.ilike(match_string))
        results = set(m.game_id for m in matches)

    return results


def delete_metadata_values(game_id):
    """
    Delete all the metadata value records for a game

    :param game_id: ID of the game to delete metadata from
    """

    with Session.begin() as session:
        # Retrieve the game - the navigation/relationship properties will ensure this loads the moves and,
        # with them, their analyses
        game = session.query(Game).get(game_id)

        # Get a list of metadata value IDs
        metadata_value_ids = [v.id for v in game.meta_data]

        # Delete them all
        session.query(MetaDataValue).filter(MetaDataValue.id.in_(metadata_value_ids)).delete(synchronize_session=False)
