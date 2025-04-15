#!/bin/bash -fß

# Create and activate a virtual environment
cd $PROJECT_ROOT
. make_venv.sh
. venv/bin/activate

# Remove and re-create the chess database data folder, if it exists
export PYTHONPATH="$PROJECT_ROOT/src"
rm -f "$PROJECT_ROOT/data/chess.db"
. "$PROJECT_ROOT/run_alembic.sh"
