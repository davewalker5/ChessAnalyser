#!/usr/bin/env bash

# Record start time (epoch seconds)
STARTED=$(date +%s)
echo "Run started at: $(date '+%Y-%m-%d %H:%M:%S')"

if [[ $# -eq 1 ]]; then
    echo "Running reports for category: $1"
fi

# Get the root of the reporting folder
export PERFORMANCE_ROOT=$( cd "$( dirname "$0" )" && pwd )

# If an (optional) "category" (i.e. report folder) has been specified, make sure
# it exists
REPORTS_FOLDER=""
if [[ $# -eq 1 ]]; then
    REPORTS_FOLDER="$PERFORMANCE_ROOT/$1"
    if [ ! -d "$REPORTS_FOLDER" ]; then
        echo "Reports folder '$1' not found"
        exit 1
    fi
fi

# Activate the virtual environment
. $PERFORMANCE_ROOT/venv/bin/activate

# Suppress warnings about the output file extension
export PYTHONWARNINGS="ignore"

# Define a list of notebooks to skip
declare -a exclusions=(
    "analysis.ipynb"
    "constants.ipynb"
    "database.ipynb"
    "export.ipynb"
    "pathutils.ipynb"
)

# Get a list of Jupyter Notebooks and iterate over them
files=$(find `pwd` -name '*.ipynb')
while IFS= read -r file; do
    # Get the notebook file name and extension without the path
    folder=$(dirname "$file")
    filename=$(basename -- "$file")

    # See if the notebook is in the exclusions list
    found=0
    if [[ " ${exclusions[@]} " =~ " $filename " ]]; then
        echo "Notebook $filename is in the exclusions list and will not be run"
        found=1
    fi

    # If this notebook isn't in the exclusions list, run it
    if [[ found -eq 0 ]]; then
        cd "$folder"
        echo "Running notebook $filename ..."
        papermill "$filename" /dev/null
    fi
done <<< "$files"

# Record end time (epoch seconds)
ENDED=$(date +%s)
echo "Run completed at: $(date '+%Y-%m-%d %H:%M:%S')"

# Calculate elapsed time in seconds
ELAPSED=$(( $ENDED - $STARTED ))

# Convert seconds into HH:MM:SS
DURATION=$(printf "%02d:%02d:%02d" $(($ELAPSED/3600)) $((($ELAPSED%3600)/60)) $(($ELAPSED%60)))
echo "Run time: $DURATION"
