WHITE = "White"
BLACK = "Black"


def get_player_for_halfmove(halfmove):
    """
    Given a halfmove count, determine which player is to play next

    :param halfmove: Halfmove number
    """
    player = WHITE if (halfmove % 2) > 0 else BLACK
    return player
