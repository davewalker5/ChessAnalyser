"""Players table

Revision ID: ebe5dd234fdd
Revises: 4f04d4da1137
Create Date: 2025-03-30 08:23:04.245482

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from chess_analyser.database.models import Player


# revision identifiers, used by Alembic.
revision: str = 'ebe5dd234fdd'
down_revision: Union[str, None] = '4f04d4da1137'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Players',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('elo', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('ai', sa.Boolean(), nullable=False, server_default="0"),
        sa.CheckConstraint('LENGTH(TRIM(name)) > 0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='PLAYER_NAME_UX')
    )

    # Get an ORM session
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # Create the default, "unknown", player
    session.add(Player(name="?", elo=0, ai=False))
    session.commit()


def downgrade() -> None:
    op.drop_table('Players')
