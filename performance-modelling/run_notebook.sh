#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
    echo Usage: run_notebook.sh NOTEBOOK
    exit 1
fi

# Activate the virtual environment
export PERFORMANCE_ROOT=$( cd "$( dirname "$0" )" && pwd )
. $PERFORMANCE_ROOT/venv/bin/activate

export PYTHONWARNINGS="ignore"
papermill "$1" /dev/null
