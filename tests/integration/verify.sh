#!/bin/bash -f

PYTHON_SCRIPT_FOLDER="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
python "$PYTHON_SCRIPT_FOLDER/verify-text-file.py" --file "$1" --type $2
exit $?
