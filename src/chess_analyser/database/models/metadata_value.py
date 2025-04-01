from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class MetaDataValue(Base):
    """
    Class representing a meta data value associated with a game
    """
    __tablename__ = "MetaDataValues"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Game item with which the value is associated
    game_id = Column(Integer, ForeignKey("Games.id"), nullable=False)
    #: Metadata item with which the value is associated
    metadata_item_id = Column(Integer, ForeignKey("MetaDataItems.id"), nullable=False)
    #: Item value
    value = Column(String, nullable=True)

    #: Parent game instance
    game = relationship("Game", back_populates="meta_data", lazy="joined")

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, game_id={self.game_id!r}, metadata_item_id={self.metadata_item_id!r}, value={self.value!r})"
