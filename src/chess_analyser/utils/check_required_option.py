def check_required_option(options, option, option_name):
    """
    Check that a required option has been supplied in an options dictionary

    :param options: Options dictionary
    :param option: Option to check
    :param option_name: Name of the option as reported in the error raised
    """
    if not options[option]:
        message = f"{option_name} is required but not specified"
        raise ValueError(message)
