from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint, Boolean
from .base import Base


class Player(Base):
    """
    Class representing a player
    """
    __tablename__ = "Players"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Player name
    name = Column(String, nullable=False, unique=True)
    #: Player ELO rating
    elo = Column(Integer, default=0, nullable=False)
    #: AI indicator
    ai = Column(Boolean, default=0, nullable=False)

    __table_args__ = (UniqueConstraint('name', name='PLAYER_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, name={self.name!r}, elo={self.elo!r}, ai={self.ai!r})"
