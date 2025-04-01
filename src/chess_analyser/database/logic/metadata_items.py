"""
Metadata item database logic
"""

from ..models import Session, MetaDataItem
import sqlalchemy as db


def list_metadata_items():
    """
    Return a list of metadata items
    """
    with Session.begin() as session:
        query = session.query(MetaDataItem)
        metadata_items = query.order_by(db.asc(MetaDataItem.id)).all()

    return metadata_items
