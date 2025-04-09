CHECK_FOR_ALL = 0
CHECK_FOR_ONE = 1


def check_required_options(options, required, mode):
    """
    Check that required options have been supplied in an options dictionary

    :param options: Options dictionary
    :param required: List of options to check
    :param mode: Option checking mode
    """

    number_specified = 0
    for option in required:
        if options[option]:
            # If the checking mode's "one of N" then just count the options that are
            # specified and validate at the end
            number_specified += 1

        elif mode == CHECK_FOR_ALL:
            # If the checking mode is "all", then any missing option is an error
            message = f"{option} is required but not specified"
            raise ValueError(message)

    if mode == CHECK_FOR_ONE and number_specified != 1:
        message = f"One of {", ".join(required)} is required but {number_specified} were specified"
        raise ValueError(message)
