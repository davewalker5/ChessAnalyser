from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint
from .base import Base


class AnalysisEngine(Base):
    """
    Class representing an analysis engine
    """
    __tablename__ = "AnalysisEngines"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Engine name
    name = Column(String, nullable=False, unique=True)

    __table_args__ = (UniqueConstraint('name', name='ANALYSISENGINE_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, name={self.name!r})"
