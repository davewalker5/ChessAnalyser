from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Analysis(Base):
    """
    Class representing the analysis for a move
    """
    __tablename__ = "Analysis"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Engine generating the analysis
    analysis_engine_id = Column(Integer, ForeignKey("AnalysisEngines.id"), nullable=False)
    #: Move the analysis relates to
    move_id = Column(Integer, ForeignKey("Moves.id"), nullable=False)
    #: Previous score
    previous_score = Column(Integer, nullable=False)
    #: Score for this move
    score = Column(Integer, nullable=False)
    #: Centipawn loss for this move
    cpl = Column(Integer, nullable=False)
    #: Win % for this move
    win_percent = Column(Float, nullable=False)
    #: Accuracy for this move
    accuracy = Column(Float, nullable=False)
    #: Evaluation of this move
    evaluation = Column(String, nullable=False)
    #: Annotation for this move
    annotation = Column(String, nullable=True)

    #: Parent move instance
    move = relationship("Move", back_populates="analyses", lazy="joined")

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, analysis_engine_id={self.analysis_engine_id!r}, " \
               f"move_id={self.move_id!r}, previous_score={self.previous_score!r}, score={self.score!r}, " \
               f"cpl={self.cpl!r}, win_percent={self.win_percent!r}, accuracy={self.accuracy!r}, " \
               f"evaluation={self.evaluation!r}, annotation={self.annotation!r})"
