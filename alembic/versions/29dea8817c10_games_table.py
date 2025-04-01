"""Games table

Revision ID: 29dea8817c10
Revises: fefca1ffa024
Create Date: 2025-03-30 08:40:21.873723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29dea8817c10'
down_revision: Union[str, None] = 'fefca1ffa024'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Games',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('reference', sa.String(), nullable=False),
        sa.Column('white_player_id', sa.Integer(), nullable=False),
        sa.Column('black_player_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('LENGTH(TRIM(reference)) > 0'),
        sa.UniqueConstraint('reference', name='GAME_REF_UX'),
        sa.ForeignKeyConstraint(['white_player_id'], ['Players.id'], ),
        sa.ForeignKeyConstraint(['black_player_id'], ['Players.id'], ),
    )


def downgrade() -> None:
    op.drop_table('Games')
