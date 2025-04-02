"""
Move analysis database logic
"""

from ...constants import get_player
from ..models import Session, Analysis, Game
from .games import load_game

MOVE_INDEX = 0
SAN_INDEX = 3
PLAYER_INDEX = 2
ANNOTATION_INDEX = 4
EVALUATION_INDEX = 8
CP_LOSS_INDEX = 9
WIN_PERCENT_INDEX = 10
ACCURACY_INDEX = 11


def create_move_analysis(analysis_engine_id, move_id, previous_score, score, cpl, win_percent, accuracy, evaluation, annotation):
    """
    Create a new analysis record

    :param analysis_engine_id: ID for the engine performing the analysis
    :param move_id: ID of the move the analysis relates to
    :param previous_score: Previous move score
    :param score: Score for this move
    :param cpl: CPL for this move
    :param win_percent: Win % for this move
    :param accuracy: Accuracy for this move
    :param evaluation: Evaluation of this move
    :param annotation: Annotation for this move
    :returns: An instance of the Analysis class for the created record
    """

    with Session.begin() as session:
        analysis = Analysis(analysis_engine_id=analysis_engine_id,
                            move_id=move_id,
                            previous_score=previous_score,
                            score=score,
                            cpl=cpl,
                            win_percent=win_percent,
                            accuracy=accuracy,
                            evaluation=evaluation,
                            annotation=annotation)
        session.add(analysis)

    return analysis


def delete_analysis(game_id, analysis_engine_id):
    """
    Delete all analysis records for a game and engine

    :param game_id: ID of the game to delete analyses for
    :param analysis_engine_id: ID for the engine that performed the analysis
    """

    with Session.begin() as session:
        try:
            # Retrieve the game - the navigation/relationship properties will ensure this loads the moves and,
            # with them, their analyses
            game = session.query(Game).get(game_id)

            # Iterate over the moves
            for move in game.moves:
                # Get the IDs for the analyses : If the engine's specified, limit to that engine. If not, get
                # them all
                if analysis_engine_id:
                    analysis_ids = [a.id for a in move.analyses if a.analysis_engine_id == analysis_engine_id]
                else:
                    analysis_ids = [a.id for a in move.analyses]

                # Delete the matching analyses
                session.query(Analysis).filter(Analysis.id.in_(analysis_ids)).delete(synchronize_session=False)


        except:
            pass


def load_analysis(identifier, analysis_engine_id):
    """
    Return a collection of analysis records for the specified game and engine

    :param identifier: Game identifier (reference or ID)
    :param analysis_engine_id: ID for the analysis engine used to do the analysis
    :return: List of analysis records, expressed as lists
    """

    # Load the game
    game = load_game(identifier)
    if not game:
        raise ValueError(f"Game {identifier} not found")

    # Iterate over the moves in the game
    analysis = []
    for i, move in enumerate(game.moves):
        # Get the analysis for this move for the specified engine
        move_analysis = [a for a in move.analyses if a.analysis_engine_id == analysis_engine_id]
        if not move_analysis:
            raise ValueError(f"Analysis for game {identifier} using engine {analysis_engine_id} not found")

        # Construct a combined move and analysis row for this move and add it to the list
        move_analysis = move_analysis[0]
        analysis.append([
            1 + i // 2,
            1 + i,
            get_player(1 + i),
            move.san,
            move_analysis.annotation,
            move.uci,
            move_analysis.previous_score,
            move_analysis.score,
            move_analysis.evaluation,
            move_analysis.cpl,
            move_analysis.win_percent,
            move_analysis.accuracy
        ])

    return analysis
