import json
import os
from pathlib import Path
import platform

# Engine dictionary
ENGINES_ROOT = "ENGINES_ROOT"   # Name of the evironment variable containing root path for engines
ENGINES_JSON = "engines.json"   # Name of the JSON file containing the definitions
DISPLAY_NAME = "name"           # Engine display name
SKIP_MATE = "skip_mate"         # If True, the final mating move is not passed to the engine for analysis
EXECUTABLE = "executable"       # Per-OS relative paths to the executable from the engines root folder

ENGINES = {}


def load_engine_definitions():
    """
    Load the engine configurations
    """
    global ENGINES
    file_path = Path(__file__).parent.parent.parent.parent.resolve() / Path(ENGINES_JSON)
    if not Path(file_path).is_file():
        raise ValueError(f"Engine definition file '{file_path}' not found")

    with open(file_path) as json_file:
        ENGINES = json.load(json_file)


def get_engine_display_name(engine):
    """
    Return the display name for an engine

    :param engines: Dictionary of engine configurations
    :param engine: Engine name passed on the CLI to the analysis method
    :return: Display name for the engine
    """
    global ENGINES
    display_name = ENGINES[engine][DISPLAY_NAME] if engine in ENGINES else "Unknown"
    return display_name


def get_engine_skip_mate(engine):
    """
    Return the "skip the mating move" flag for an engine

    :param engines: Dictionary of engine configurations
    :param engine: Engine name passed on the CLI to the analysis method
    """
    global ENGINES
    skip_mating_move = ENGINES[engine][SKIP_MATE] if engine in ENGINES else True
    return skip_mating_move


def get_engine_path(engine):
    """
    Return the full path for an engine

    :param engines: Dictionary of engine configurations
    :param engine: Engine name passed on the CLI to the analysis method
    """
    global ENGINES
    engine_path = None

    # Check the engine is supported
    if ENGINES_ROOT not in os.environ:
        raise EnvironmentError(f"{ENGINES_ROOT} environment variable is not set")
    elif engine not in ENGINES:
        raise ValueError(f"Unknown engine: {engine}")
    else:
        # Get the OS name and extract the relative path to the engine on this platform
        os_name = platform.system()
        executables = ENGINES[engine][EXECUTABLE]
        relative_path = executables[os_name] if os_name in executables else None

        # Check the engine's path is defined for this platform
        if relative_path:
            # For path objects, "/" is overloaded to concatenate the paths and the
            # resolve() method gives an absolute path. The separators in the result
            # are normalised for the current OS by Path()
            engines_root = os.environ[ENGINES_ROOT]
            engine_path = (Path(engines_root) / Path(relative_path)).resolve()

            # Check the executable exists
            if not Path(engine_path).is_file():
                print(f"'{engine_path}' not found")
                engine_path = None

        else:
            raise NotImplementedError(f"{engine} is not supported on this OS ({os_name})")

    return engine_path
