#!/bin/bash -f

if (( $# != 1 )); then
    echo Usage: load-pgn-folder.sh FOLDER_PATH ENGINE
    exit 1
fi

# Define the list of engines to analyse with
declare -a engines=(
    "dragon"
    "komodo"
    "rubichess"
    "stockfish"
)

# Set the environment so Python can find the analyser module
PROJECT_ROOT="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="$PROJECT_ROOT/src"

# Activate the virtual environment and run the command
. "$PROJECT_ROOT/venv/bin/activate"

# Get a list of patching PGN file names and iterate over them
files=$(find "$1" -name '*.pgn')
while IFS= read -r file; do
    # Get the full path and extract the file name without extension to use as the reference
    fullpath=$(readlink -f "$file")
    filename=$(basename -- "$file")
    reference=${filename%.*}

    # Import the PGN file
    echo "Importing '$filename' using reference '$reference'"
    python -m chess_analyser --load --pgn "$fullpath" --reference "$reference"

    # Iterate over the engines
    for engine in ${!engines[*]}; do
        echo "Analysing game '$reference' with ${engines[$engine]}"
        python -m chess_analyser --analyse --reference "$reference" --engine "${engines[$engine]}"
    done
done <<< "$files"
