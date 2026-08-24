#!/bin/bash -f

# Set the environment so Python can find the analyser module
PROJECT_ROOT="$( cd -- "$(dirname "$0")/.." >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="$PROJECT_ROOT/src"

# Activate the virtual environment and run the command
. "$PROJECT_ROOT/venv/bin/activate"

# Run the PGN editor
python -m pgn_editor
