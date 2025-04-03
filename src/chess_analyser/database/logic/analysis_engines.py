"""
Analysis engine database logic
"""

from ..models import Session, AnalysisEngine
from functools import singledispatch


def create_analysis_engine(name):
    """
    Create a new analysis_engine

    :param name: Player name
    :returns: An instance of the AnalysisEngine class for the created record
    """
    with Session.begin() as session:
        analysis_engine = AnalysisEngine(name=name)
        session.add(analysis_engine)

    return analysis_engine


@singledispatch
def get_analysis_engine(_):
    """
    Return the AnalysisEngine instance for the player with the specified identifier

    :param _: AnalysisEngine name or ID
    :return: Instance of the engine
    """
    raise TypeError("Invalid parameter type")


@get_analysis_engine.register(str)
def _(name):
    try:
        with Session.begin() as session:
            analysis_engine = session.query(AnalysisEngine).filter(AnalysisEngine.name == name).one()

    except:
        analysis_engine = None

    return analysis_engine


@get_analysis_engine.register(int)
def _(id):
    with Session.begin() as session:
        analysis_engine = session.query(AnalysisEngine).get(id)

    return analysis_engine


def get_analysis_engine_id(name, create_if_not_found=False):
    """
    Retrieve a named analysis engine

    :param name: Analysis engine name
    :param create_if_not_found: If True, the engine will be created if it doesn't already exist
    :return: Analysis engine ID
    """
    analysis_engine = get_analysis_engine(name)
    if not analysis_engine:
        if create_if_not_found:
            analysis_engine = create_analysis_engine(name)
        else:
            raise ValueError(f"Engine '{name}' does not exist")

    return analysis_engine.id
