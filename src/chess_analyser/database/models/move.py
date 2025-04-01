from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Move(Base):
    """
    Class representing a move associated with a game
    """
    __tablename__ = "Moves"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Game item with which the value is associated
    game_id = Column(Integer, ForeignKey("Games.id"), nullable=False)
    #: Halfmove number
    halfmove = Column(Integer, nullable=False)
    #: SAN for the move
    san = Column(String, nullable=False)
    #: UCI notation for the move
    uci = Column(String, nullable=False)

    #: Parent game instance
    game = relationship("Game", back_populates="moves", lazy="joined")

    #: Analyses associated with this game
    analyses = relationship("Analysis",
                            back_populates="move",
                            cascade="all, delete, delete-orphan",
                            lazy="joined")

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, game_id={self.game_id!r}, halfmove={self.halfmove!r}, san={self.san!r}, uci={self.uci!r})"
