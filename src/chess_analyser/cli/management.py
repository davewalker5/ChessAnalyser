from ..constants import OPT_ENGINE, OPT_REFERENCE, OPT_VERBOSE, OPT_METADATA, OPT_VALUE
from ..management import GAME, ANALYSIS, delete_data, update_metadata_value
from ..utils import check_required_options, CHECK_FOR_ALL


def confirm(targets):
    """
    Confirm deletion of data

    :param targets: List of targets for deletion
    :return: True if confirmed
    """
    # Initialise the valid inputs and the confirmed response
    confirmed = "y"
    valid_inputs = [confirmed, "Y", "n", "N"]

    # Loop until the user provides a valid response
    response = None
    prompt = f"Are you sure you want to delete {targets}? [{'/'.join(valid_inputs)}] "
    while not response in valid_inputs:
        # Prompt for confirmation
        response = input(prompt)
        if response in valid_inputs:
            return response == confirmed


def dispatch_delete(options):
    """
    Delete a game or the analysis of that game by an engine

    :param options: Dictionary of deletion options
    """
    # The game reference must be specified
    check_required_options(options, [OPT_REFERENCE], CHECK_FOR_ALL)

    print()
    if  options[OPT_ENGINE]:
        # If the engine is specified, just delete the analysis of that game for that engine
        confirmed = confirm(f"the analysis of game {options[OPT_REFERENCE]} for engine {options[OPT_ENGINE]}")
        if confirmed:
            delete_data(options[OPT_REFERENCE], ANALYSIS, options[OPT_ENGINE], options[OPT_VERBOSE])
    else:
        # If the engine isn't specified, all data relating to the game is deleted
        confirmed = confirm(f"all data relating to game {options[OPT_REFERENCE]}")
        if confirmed:
            delete_data(options[OPT_REFERENCE], GAME, None, options[OPT_VERBOSE])


def dispatch_set_metadata(options):
    """
    Set a metadata value

    :param options: Dictionary of options
    """
    # The game reference must be specified
    check_required_options(options, [OPT_REFERENCE, OPT_METADATA, OPT_VALUE], CHECK_FOR_ALL)

    # Update the metadata value
    update_metadata_value(options[OPT_REFERENCE], options[OPT_METADATA], options[OPT_VALUE], options[OPT_VERBOSE])
