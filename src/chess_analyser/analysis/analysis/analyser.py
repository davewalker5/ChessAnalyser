from ...constants import INITIAL_SCORE, OPT_REFERENCE, OPT_ENGINE, OPT_VERBOSE, get_player
from ...database.logic import load_game, delete_analysis, create_move_analysis, get_analysis_engine_id
from ...engines import load_engine_definitions, get_engine_path, get_engine_skip_mate, get_engine_display_name
from ...reporting import print_analysis_table_headers, print_analysis_table_row
from .scoring import calculate_normalised_score, calculate_cp_loss, calculate_win_percent, \
    calculate_accuracy, get_annotation
import chess
import chess.engine
import chess.pgn
import os

# Members of the per-move analysis dictionary
ANALYSIS_MOVE_ID = "move_id"
ANALYSIS_PREV_SCORE = "previous_score"
ANALYSIS_SCORE = "score"
ANALYSIS_CPL = "cp_loss"
ANALYSIS_WIN_PERCENT = "win_percent"
ANALYSIS_ACCURACY = "accuracy"
ANALYSIS_EVALUATION = "evaluation"
ANALYSIS_ANNOTATION = "annotation"

# Engine and scoring control
TIME_LIMIT_MS = 500


class _suppress_stdout_stderr(object):
    '''
    Method taken from the following Stack Overflow post:

    https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions

    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.

    This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      
    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)


def store_analysis(game_id, engine_name, analysis):
    # Get the engine ID and delete any previous analysis for this game and engine
    engine_id = get_analysis_engine_id(engine_name)
    delete_analysis(game_id, engine_id)

    # Save the analysis records
    for move_analysis in analysis:
        _ = create_move_analysis(
            engine_id,
            move_analysis[ANALYSIS_MOVE_ID],
            move_analysis[ANALYSIS_PREV_SCORE],
            move_analysis[ANALYSIS_SCORE],
            move_analysis[ANALYSIS_CPL],
            move_analysis[ANALYSIS_WIN_PERCENT],
            move_analysis[ANALYSIS_ACCURACY],
            move_analysis[ANALYSIS_EVALUATION],
            move_analysis[ANALYSIS_ANNOTATION])


def analyse_game(options):
    """
    Analyse a game that's been previously imported into the database, given its ID
    
    :param options: Dictionary of analysis parameters
    """

    # Load the game
    game = load_game(options[OPT_REFERENCE])
    if not game:
        raise ValueError(f"Game {options[OPT_REFERENCE]} not found")

    # Relationship/navigation properties should load the moves
    if not game.moves:
        raise ValueError(f"No moves found for the game with ID {game.id}")

    # Get the path to the engine
    load_engine_definitions()
    engine_path = get_engine_path(options[OPT_ENGINE])

    # Set the initial "previous score" and evaluation
    prev_score_object = chess.engine.PovScore(chess.engine.Cp(INITIAL_SCORE), chess.WHITE)

    # Initialise the analysis results list and the lists used to construct the annotated
    # version of the PGN file
    analysis = []

    # Open the engine. Suppressing stdout and stderr suppresses any banners and startup messages
    with _suppress_stdout_stderr():
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    # Determine if the mating move should be passed to the engine for analysis
    skip_mating_move = get_engine_skip_mate(options[OPT_ENGINE])

    # Print the column headers for the tabulated analysis results
    if options[OPT_VERBOSE]:
        engine_display_name = get_engine_display_name(options[OPT_ENGINE])
        print(f"\nAnalysing game '{game.reference}' (#{game.id}) using {engine_display_name}\n\n")
        print_analysis_table_headers()

    board = chess.Board()
    for move in game.moves:
        # Determine the player making the current move
        player = get_player(move.halfmove)

        # Initialise the evaluation
        annotation = ""
        evaluation = ""

        # Make and assess the move, checking that the engine can cope with the mating move if that's
        # what this is
        board.push_uci(move.uci)
        if not (board.is_checkmate() and skip_mating_move):
            # Pass the move to the engine for analysis
            info = engine.analyse(board, chess.engine.Limit(time=(TIME_LIMIT_MS / 1000.0)))

            # Extract the scoring information from the response
            if "score" in info:
                score_object = info["score"]

                # Normalise the score and calculate the centipawn loss, accuracy and annotation
                normalised_prev_score, _ = calculate_normalised_score(prev_score_object, player)
                normalised_score, evaluation = calculate_normalised_score(score_object, player)
                cp_loss = calculate_cp_loss(normalised_prev_score, normalised_score)
                prev_win_percent = calculate_win_percent(normalised_prev_score)
                win_percent = calculate_win_percent(normalised_score)
                accuracy = calculate_accuracy(prev_win_percent, win_percent)
                annotation = get_annotation(prev_win_percent, win_percent)

                # Capture the previous score object
                prev_score_object = score_object

        # Capture the analysis results for this move
        analysis.append({
            ANALYSIS_MOVE_ID: move.id,
            ANALYSIS_PREV_SCORE: normalised_prev_score,
            ANALYSIS_SCORE: normalised_score,
            ANALYSIS_CPL: cp_loss,
            ANALYSIS_WIN_PERCENT: win_percent,
            ANALYSIS_ACCURACY: accuracy,
            ANALYSIS_EVALUATION: evaluation,
            ANALYSIS_ANNOTATION: annotation
        })

        # Optionally, output the row to the console
        if options[OPT_VERBOSE]:
            row = [
                1 + move.halfmove // 2,
                move.halfmove,
                player,
                move.san,
                annotation,
                move.uci,
                normalised_prev_score,
                normalised_score,
                evaluation,
                cp_loss,
                win_percent,
                accuracy
            ]
            print_analysis_table_row(row)

    # Close the engine
    engine.quit()

    # Store the analysis
    store_analysis(game.id, options[OPT_ENGINE], analysis)
