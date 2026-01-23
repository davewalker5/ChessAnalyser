from math import exp

MOVES_SHORT = 25
ACPL_MIN_SHORT = 25
ACPL_MIN_NORMAL = 20
R_MIN = 800
R_MAX = 2300
K = 0.05341958625524604
ACPL_BEST = 23.709467837259233


def prompt_for_number(prompt, data_type_name, converter, minimum_value=None, maximum_value=None):
    """
    Prompt for an number

    :param prompt: User-friendly prompt
    :param data_type_name: Name of the data type
    :param converter: Function to use to convert the user input to a number
    :param minimum_value: Minimum acceptable value
    :param maximum_value: Maximum acceptable value
    :return: Numeric value or None if cancelled
    """
    while True:
        try:
            # Prompt for user input - if the input is empty, return nothing
            user_input = input(prompt + ("?" if not prompt.endswith("?") else "") + " ")
            if user_input == "":
                return None

            # Convert to an integer
            number = converter(user_input)
            if minimum_value and number < minimum_value:
                print("Number must be >= ", minimum_value)
            elif maximum_value and number > maximum_value:
                print("Number must be <= ", maximum_value)
            else:
                return number

        except ValueError:
            print("Please enter a valid " + data_type_name)


def calculate_performance(acpl, game_length):
    """
    Given an ACPL, calculate and return the performance rating
    
    :param acpl: ACPL to use to calculate performance
    :param game_length: Number of moves in the game
    :return: Numeric performance rating for that ACPL
    """
    acpl_floor = ACPL_MIN_SHORT if game_length < MOVES_SHORT else ACPL_MIN_NORMAL
    acpl_effective = acpl_floor if acpl < acpl_floor else acpl
    return int(R_MIN + (R_MAX - R_MIN) * exp(-K * (acpl_effective - ACPL_BEST)) + 0.5)


def print_title(title):
    """
    Display an application title

    :param title: Application title
    """
    print()
    print("=" * len(title))
    print(title)
    print("=" * len(title))
    print()


def main():
    """
    Wrapper round the chess performance calculator
    """
    print_title("Chess Performance Calculator")
    while True:
        acpl = prompt_for_number("ACPL", "number", float, 0.0, None)
        if acpl is None:
            return

        game_length = prompt_for_number("Moves", "integer", int, 0, None)
        if game_length is None:
            return

        performance_rating = calculate_performance(acpl, game_length)

        print()
        print("Performance rating = " + str(performance_rating))
        print()


main()
