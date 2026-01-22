from math import exp

R_MIN = 800
R_MAX = 2300
K = 0.0485420171014147
ACPL_BEST = 13.383123697788


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


def calculate_performance(acpl):
    """
    Given an ACPL, calculate and return the performance rating
    
    :param acpl: ACPL to use to calculate performance
    :return: Numeric performance rating for that ACPL
    """
    return int(R_MIN + (R_MAX - R_MIN) * exp(-K * (acpl - ACPL_BEST)) + 0.5)


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

        performance_rating = calculate_performance(acpl)

        print()
        print("ACPL " + str(acpl) + " => Rating " + str(performance_rating))
        print()


main()
