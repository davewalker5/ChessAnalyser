from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, CheckConstraint
from .base import Base


class MetaDataItem(Base):
    """
    Class representing a meta data item that can be associated with a game
    """
    __tablename__ = "MetaDataItems"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Item name
    name = Column(String, nullable=False, unique=True)
    #: Display order when eriting to PGNs or tabulating meta data
    display_order = Column(Integer, nullable=False, unique=True)
    #: Flag indicating this is a standard PGN file header item
    is_pgn = Column(Boolean, nullable=False, default=True)
    #: Default value for this item
    default_value = Column(String, nullable=True)

    __table_args__ = (UniqueConstraint('name', name='METADATA_ITEM_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, name={self.name!r}, display_order={self.display_order!r}, is_pgn={self.is_pgn!r}, default_value={self.default_value!r})"
