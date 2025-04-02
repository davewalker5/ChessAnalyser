"""
Metadata value database logic
"""

from ..models import Session, MetaDataValue


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
