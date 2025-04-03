"""Mark FEN as a non-standard PGN header

Revision ID: e99865562d6c
Revises: 9741fcc800ae
Create Date: 2025-04-03 06:45:46.210127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e99865562d6c'
down_revision: Union[str, None] = '9741fcc800ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get an ORM session
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # Update the metadata item
    session.execute(sa.text("UPDATE MetaDataItems SET is_pgn = 0 WHERE name='FEN'"))
    session.commit()


def downgrade() -> None:
    # Get an ORM session
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # Update the metadata item
    session.execute(sa.text("UPDATE MetaDataItems SET is_pgn = 1 WHERE name='FEN'"))
    session.commit()
