#!/bin/bash -f

# Set the environment
PROJECT_ROOT="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="$PROJECT_ROOT/src"

# Activate the virtual environment
. "$PROJECT_ROOT/venv/bin/activate"

# Make sure the data folder exists
if [ ! -d "$PROJECT_ROOT/data" ]; then
  mkdir -p "$PROJECT_ROOT/data"
fi

# Run Alembic to create the database / apply the latest migrations
alembic upgrade head
