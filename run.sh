#!/bin/bash -f

# Set the environment so Python can find the analyser module
PROJECT_ROOT="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="$PROJECT_ROOT/src"

# Activate the virtual environment and run the command
. "$PROJECT_ROOT/venv/bin/activate"

# Create an array containing the arguments - this is to ensure spaces in arguments don't cause
# issues with the command line parser when the argements are passed to it
i=0
options=()
for arg in "$@"; do
    options[$i]="$arg"
    i=$((i + 1))
done

# Run the requested operation
python -m chess_analyser "${options[@]}"
