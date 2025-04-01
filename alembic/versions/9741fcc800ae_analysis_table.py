"""Analysis table

Revision ID: 9741fcc800ae
Revises: 175be63b0ba1
Create Date: 2025-03-30 15:28:28.364468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9741fcc800ae'
down_revision: Union[str, None] = '175be63b0ba1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Analysis',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('analysis_engine_id', sa.Integer(), nullable=False),
        sa.Column('move_id', sa.Integer(), nullable=False),
        sa.Column('previous_score', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('cpl', sa.Integer(), nullable=False),
        sa.Column('win_percent', sa.Float(), nullable=False),
        sa.Column('accuracy', sa.Float(), nullable=False),
        sa.Column('evaluation', sa.String(), nullable=False),
        sa.Column('annotation', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['move_id'], ['Moves.id'], ),
        sa.ForeignKeyConstraint(['analysis_engine_id'], ['AnalysisEngines.id'], ),
    )


def downgrade() -> None:
    op.drop_table('Analysis')
