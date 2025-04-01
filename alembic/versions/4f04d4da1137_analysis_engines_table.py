"""Engines table

Revision ID: 4f04d4da1137
Revises: 
Create Date: 2025-03-30 08:14:50.422884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f04d4da1137'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'AnalysisEngines',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.CheckConstraint('LENGTH(TRIM(name)) > 0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='ANALYSISENGINE_NAME_UX')
    )


def downgrade() -> None:
    op.drop_table('AnalysisEngines')
