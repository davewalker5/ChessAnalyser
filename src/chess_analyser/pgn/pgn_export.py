from ..constants import INITIAL_SCORE, OPT_REFERENCE, OPT_ENGINE, OPT_PGN, OPT_VERBOSE
from ..utils import get_player_for_halfmove, WHITE, check_required_options, CHECK_FOR_ALL
from ..database.logic import load_game
from ..reporting import load_game_information
from ..analysis.analysis import calculate_normalised_score
from ..database.logic import get_analysis_engine_id
import chess
import chess.engine

MAX_LINE_LENGTH = 120


def export_pgn(options):
    """
    Export a PGN file including analysis results

    :param options: Dictionary of export options
    """

    # Check the required options have been supplied
    check_required_options(options, [OPT_REFERENCE, OPT_ENGINE, OPT_PGN], CHECK_FOR_ALL)

    if options[OPT_VERBOSE]:
        print(f"\nExporting annotated PGN\n")
        print(f"Game reference  : {options[OPT_REFERENCE]}")
        print(f"Analysis engine : {options[OPT_ENGINE]}")
        print(f"PGN file        : {options[OPT_PGN]}")
        print("\nLoading game ...")

    # Load the game
    game = load_game(options[OPT_REFERENCE])
    if not game:
        raise ValueError(f"Game {options[OPT_REFERENCE]} not found")

    # Relationship/navigation properties should load the moves
    if not game.moves:
        raise ValueError(f"No moves found for the game with ID {game.id}")

    # Get the game headers
    if options[OPT_VERBOSE]:
        print("Loading game metadata ...")
    headers = load_game_information(options[OPT_REFERENCE], True, None, False)
    result_list = [h[1] for h in headers if h[0] == "Result"]
    result = result_list[0] if result_list else "*"

    # Create an initial score object and get the initial evaluation
    initial_score_object = chess.engine.PovScore(chess.engine.Cp(INITIAL_SCORE), chess.WHITE)
    _, initial_evaluation = calculate_normalised_score(initial_score_object, WHITE)

    # Get a list of evaluations and annotations, one per move, for the specified engine
    if options[OPT_VERBOSE]:
        print("Compiling move annotations and evaluations ...")

    evaluations = []
    annotations = []
    analysis_engine_id = get_analysis_engine_id(options[OPT_ENGINE])
    for i, move in enumerate(game.moves):
        move_analysis = [a for a in move.analyses if a.analysis_engine_id == analysis_engine_id][0]
        evaluations.append(move_analysis.evaluation)
        annotations.append(move_analysis.annotation)

    # Open the PGN file
    if options[OPT_VERBOSE]:
        print("Writing PGN file ...")

    with open(options[OPT_PGN], "w") as file:
        # Write the headers
        for header in headers:
            file.write(f"[{header[0]} \"{header[1]}\"]\n")

        file.write("\n")

        # The first evaluation is for the position before white's first move, and is written at the
        # head of the move list
        line = f"{{[%eval {initial_evaluation}]}} "

        # Iterate over the halfmoves
        for i, move in enumerate(game.moves):
            # Format the evaluation string for this halfmove
            evaluation = f"{{[%eval {evaluations[i]}]}}" if evaluations[i] else ""

            # Format the move text based on which player has the current turn
            player = get_player_for_halfmove(i + 1)
            if player == WHITE:
                move_text = f"{1 + i // 2}. {move.san}{annotations[i]} {evaluation} "
            else:
                move_text = f"{move.san}{annotations[i]} {evaluation} "

            # Wrap text when we reach the line length limit
            if (len(line) + len(move_text)) > MAX_LINE_LENGTH:
                file.write(f"{line}\n")
                line = ""

            line += move_text

        # Here, the line may contain the final part of the game and so must be written to
        # finish off the file
        file.write(f"{line} {result}\n")
