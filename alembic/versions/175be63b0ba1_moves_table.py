"""Moves table

Revision ID: 175be63b0ba1
Revises: 0bc8b67a875a
Create Date: 2025-03-30 09:10:46.085435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '175be63b0ba1'
down_revision: Union[str, None] = '0bc8b67a875a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Moves',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('halfmove', sa.Integer(), nullable=False),
        sa.Column('san', sa.String(), nullable=False),
        sa.Column('uci', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['game_id'], ['Games.id'], )
    )


def downgrade() -> None:
    op.drop_table('Moves')
