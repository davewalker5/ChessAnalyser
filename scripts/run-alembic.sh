#!/bin/bash -f

# Set the environment
PROJECT_ROOT="$( cd -- "$(dirname "$0")/.." >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="$PROJECT_ROOT/src"
cd "$PROJECT_ROOT"

# Activate the virtual environment
. /venv/bin/activate

# Make sure the data folder exists
if [ ! -d "$PROJECT_ROOT/data" ]; then
  mkdir -p data
fi

# Run Alembic to create the database / apply the latest migrations
alembic upgrade head
