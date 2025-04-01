#!/bin/bash -f

DOCS_FOLDER="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_ROOT="$DOCS_FOLDER/.."
export PYTHONPATH="$PROJECT_ROOT/src"

echo "Documents Folder : $DOCS_FOLDER"
echo "Project Root     : $PROJECT_ROOT"
echo "Python Path      : $PYTHONPATH"

# The assumption is there is already a virtual environment with the requirements to
# run the analyser installed. This simply activates it and adds in the Sphinx requirements
. "$PROJECT_ROOT/venv/bin/activate"
pip install -r requirements.txt

# Delete and re-create the code documentation
rm -fr source/code
sphinx-apidoc -o "$DOCS_FOLDER/source/code" "$PROJECT_ROOT/src/chess_analyser"

# Build the documentation
make html
deactivate
