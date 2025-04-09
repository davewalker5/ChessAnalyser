from ...utils import WHITE
import math


MATE_SCORE = 1000


def sign(x):
    """
    Given a value, x, return the sign of that value

    :param x: Value
    :return: -1 if x < 0, 1 if x > 0, 0 if x = 0
    """
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def min_max(value, minimum, maximum):
    """
    Given a value and a range, return the value clipped to the specified range 

    :param value: Value to compare to the range
    :param minimum: Minimum of the range
    :param maximum: Maximum of the range
    :return: v if min <= v <= max, min if v < min, max if v > max
    """
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value


def calculate_normalised_score(score, player):
    """
    Given a scoring object returned by the Chess Engine and a player, calculate the normalised
    score from that player's perspective and the evaluation of the move

    :param score: PovScore object from Python-Chess
    :param player: WHITE or BLACK
    :return: Tuple of normalised cp score, evaluation string
    """
    pov_score = score.white() if player == WHITE else score.black()
    cp = pov_score.score(mate_score=MATE_SCORE)

    if score.is_mate():
        cp = MATE_SCORE * sign(cp)
        evaluation_string = f"#{abs(pov_score.mate())}"
    else:
        evaluation = abs(cp) / 100.0
        evaluation_string = f"{evaluation:+.2f}"

    normalised_cp = min_max(cp, -MATE_SCORE, MATE_SCORE)

    return normalised_cp, evaluation_string


def calculate_cp_loss(prev_score, score):
    """
    Given normalised scores for the current and previous move for a player, calculate the cp
    loss resulting from making the move

    :param prev_score: Normalised score for the previous move
    :param score: Normalised score after making the current move
    :return: The centipawn loss
    """
    score_difference = prev_score - score
    cp_loss = max(0, score_difference)
    return cp_loss


def calculate_win_percent(score):
    """
    Calculate the chance of winning % from a normalised score, per the Lichess documentation
    at https://lichess.org/page/accuracy

    :param score: Normalised score
    :return: % chance of winning
    """
    win_percent = 50 + 50 * (2 / (1 + math.exp(-0.00368208 * score)) - 1)
    return win_percent 


def calculate_accuracy(prev_win_percent, win_percent):
    """
    Calculate the accuracy of a move given the % chance of winning for the previous and current
    moves, per the Lichess documentation at https://lichess.org/page/accuracy

    :param prev_win_percent: % chance of winning for the previous move
    :param win_percent: % chance of winning for the current move
    :return: Accuracy %
    """
    accuracy = 103.1668 * math.exp(-0.04354 * (prev_win_percent - win_percent)) - 3.1669 + 1
    normalised_accuracy = min_max(accuracy, 0, 100)
    return normalised_accuracy


def get_annotation(prev_win_percent, win_percent):
    """
    Determine the annotation for a move
    
    :param prev_win_percent: % chance of winning for the previous move
    :param win_percent: % chance of winning for the current move
    :return: Annotation - ?!, ?, ??
    """
    win_percent_difference = prev_win_percent - win_percent
    if win_percent_difference > 20:
        return "??"
    elif win_percent_difference > 10:
        return "?"
    elif win_percent_difference > 5:
        return "?!"
    return ""

