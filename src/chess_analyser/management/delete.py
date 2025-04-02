from ..database.logic import load_game, delete_analysis, delete_moves, \
    delete_metadata_values, delete_game, get_analysis_engine_id


# Define bit flags indicating which items should be deleted
GAME     = 0b0001  # 1
MOVES    = 0b0010  # 2
ANALYSIS = 0b0100  # 4


def delete_data(identifier, flags, engine):
    """
    Delete aspects of a game

    :param identifier: Game identifier (reference or ID)
    :param flags: Bit flags indicating which elements to delete (GAME, MOVES, ANALYSIS)
    :param engine: Name of the analysis engine for which to delete the analysis
    """
    if not flags:
        # If the flags aren't set, there's nothing to delete!
        raise ValueError("Nothing specified for deletion")

    if flags & GAME:
        # If we're deleting the game, we need to remove the moves as well
        flags |= MOVES

    if flags & MOVES:
        # If we're deleting the moves, we need to remove the analysis as well and the passed engine is irrelevant
        flags |= ANALYSIS
        engine = None

    # Load the game
    game = load_game(identifier)
    if not game:
        raise ValueError(f"Game {identifier} not found")

    # Delete in an order that will avoid violating foreign key constraints
    if flags & ANALYSIS:
        analysis_engine_id = get_analysis_engine_id(engine) if engine != "*" else None
        delete_analysis(game.id, analysis_engine_id)

    if flags & MOVES:
        delete_moves(game.id)

    if flags & GAME:
        delete_metadata_values(game.id)
        delete_game(game.id)
