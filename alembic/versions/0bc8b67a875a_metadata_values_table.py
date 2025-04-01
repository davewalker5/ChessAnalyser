"""Metadata values table

Revision ID: 0bc8b67a875a
Revises: 29dea8817c10
Create Date: 2025-03-30 09:00:40.731845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bc8b67a875a'
down_revision: Union[str, None] = '29dea8817c10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'MetaDataValues',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('metadata_item_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['game_id'], ['Games.id'], ),
        sa.ForeignKeyConstraint(['metadata_item_id'], ['MetaDataItems.id'], )
    )


def downgrade() -> None:
    op.drop_table('MetaDataValues')
