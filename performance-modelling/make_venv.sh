#!/bin/bash -f

PERFORMANCE_MODELLING_ROOT=$( cd "$( dirname "$0" )" && pwd )

# Deactivate and remove the old virtual environment, if present
echo "Removing existing Virtual Environment, if present ..."
deactivate 2> /dev/null || true
rm -fr "$PERFORMANCE_MODELLING_ROOT/venv"

# Create a new environment and activate it
echo "Creating new Virtual Environment ..."
python -m venv "$PERFORMANCE_MODELLING_ROOT/venv"
. "$PERFORMANCE_MODELLING_ROOT/venv/bin/activate"

# Make sure packaging tools are up to date
pip install --upgrade pip setuptools

# Install the reporting suite dependencies
pip install --no-build-isolation -e "$PERFORMANCE_MODELLING_ROOT"
