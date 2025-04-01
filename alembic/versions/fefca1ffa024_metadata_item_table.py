"""Metadata item table

Revision ID: fefca1ffa024
Revises: ebe5dd234fdd
Create Date: 2025-03-30 08:30:46.878199

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from chess_analyser.database.models import MetaDataItem


# revision identifiers, used by Alembic.
revision: str = 'fefca1ffa024'
down_revision: Union[str, None] = 'ebe5dd234fdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the table
    op.create_table(
        'MetaDataItems',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('is_pgn', sa.Boolean(), nullable=False, server_default="0"),
        sa.Column('default_value', sa.String(), nullable=True),
        sa.CheckConstraint('LENGTH(TRIM(name)) > 0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='METADATA_ITEM_NAME_UX')
    )

    # Define the default metadata items as dictionaries where the key is the name
    # and the value is a dictionary of properties for the item
    metadata_items= {
        "Event": {
            "IsPGN": True,
            "Order": 1,
            "Default": "Unknown"
        },
        "Site": {
            "IsPGN": True,
            "Order": 2,
            "Default": "?"
        },
        "Date": {
            "IsPGN": True,
            "Order": 3,
            "Default": "????.??.??"
        },
        "Round": {
            "IsPGN": True,
            "Order": 4,
            "Default": "?"
        },
        "White": {
            "IsPGN": True,
            "Order": 5,
            "Default": "?"
        },
        "Black": {
            "IsPGN": True,
            "Order": 6,
            "Default": "?"
        },
        "Result": {
            "IsPGN": True,
            "Order": 7,
            "Default": "*"
        },
        "FEN": {
            "IsPGN": True,
            "Order": 8,
            "Default": ""
        },
        "PGN": {
            "IsPGN": False,
            "Order": 9,
            "Default": "?"
        }
    }

    # Get an ORM session
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # Create the default set of metadata items
    for name, properties in metadata_items.items():
        session.add(MetaDataItem(name=name, display_order=properties["Order"], is_pgn=properties["IsPGN"], default_value=properties["Default"]))
    session.commit()


def downgrade() -> None:
    op.drop_table('MetaDataItems')
