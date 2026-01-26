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

# Define a list of notebooks to run, in order
declare -a notebooks=(
    "multi_engine_performance_model.ipynb"
    "single_engine_performance_model.ipynb"
    "performance_over_time.ipynb"
)

# Iterate over them
for notebook in "${notebooks[@]}"; do
    echo "Running notebook $filename ..."
    papermill "$PERFORMANCE_ROOT/$notebook" /dev/null
done

# Record end time (epoch seconds)
ENDED=$(date +%s)
echo "Run completed at: $(date '+%Y-%m-%d %H:%M:%S')"

# Calculate elapsed time in seconds
ELAPSED=$(( $ENDED - $STARTED ))

# Convert seconds into HH:MM:SS
DURATION=$(printf "%02d:%02d:%02d" $(($ELAPSED/3600)) $((($ELAPSED%3600)/60)) $(($ELAPSED%60)))
echo "Run time: $DURATION"
