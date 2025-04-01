from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Game(Base):
    """
    Class representing a game
    """
    __tablename__ = "Games"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Game reference
    reference = Column(String, nullable=False, unique=True)
    #: ID of the white player
    white_player_id = Column(Integer, ForeignKey("Players.id"), nullable=False)
    #: ID of the black player
    black_player_id = Column(Integer, ForeignKey("Players.id"), nullable=False)

    __table_args__ = (UniqueConstraint('reference', name='GAME_REF_UX'),
                      CheckConstraint("LENGTH(TRIM(reference)) > 0"))

    #: Metadata associated with this game
    meta_data = relationship("MetaDataValue",
                             back_populates="game",
                             cascade="all, delete, delete-orphan",
                             lazy="joined")

    #: Moves associated with this game
    moves = relationship("Move",
                         back_populates="game",
                         cascade="all, delete, delete-orphan",
                         lazy="joined")

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, reference={self.reference!r}, white_player_id={self.white_player_id!r}, black_player_id={self.black_player_id!r})"
