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
