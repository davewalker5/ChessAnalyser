#!/bin/bash -f

# Check the file path and analysis engine have been specified
if (( $# != 2 )); then
    echo Usage: $0 PGN_FILE_PATH ENGINE
    exit 1
fi

# Absolute path to the PGN file has to be determined *before* changing to the
# project root to run the tests, as it's relative to wherever the script is
# run from
PGN_FILE=$(python -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1")

# Run the tests from the project root
INTEGRATION_TESTS_FOLDER="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$INTEGRATION_TESTS_FOLDER/../.."
export PROJECT_ROOT=$(pwd -P)

# Set the remaining properties to be used during the tests
TEST_RESULTS_FOLDER="$PROJECT_ROOT/tests/results"
REFERENCE="Integration Tests"
ANALYSIS_ENGINE="$2"
EXPORT_FILE_STEM="integration"

# Report the test parameters
echo
echo "Project Root             : $PROJECT_ROOT"
echo "Integration Tests Folder : $INTEGRATION_TESTS_FOLDER"
echo "Test Results Folder      : $TEST_RESULTS_FOLDER"
echo "PGN File                 : $PGN_FILE"
echo "Imported Game Reference  : $REFERENCE"
echo "Analysis Engine          : $ANALYSIS_ENGINE"
echo "Exported Test File Stem  : $EXPORT_FILE_STEM"
echo "Working Directory        : $(pwd -P)"
echo

# Delete and re-create the test results folder to remove pre-existing results, if any
rm -fr "$TEST_RESULTS_FOLDER"
if [ ! -d "$TEST_RESULTS_FOLDER" ]; then
  mkdir -p "$TEST_RESULTS_FOLDER"
fi

# Perform the tests
. "$INTEGRATION_TESTS_FOLDER/prepare.sh"
. "$INTEGRATION_TESTS_FOLDER/load.sh"
. "$INTEGRATION_TESTS_FOLDER/analyse.sh"
. "$INTEGRATION_TESTS_FOLDER/report.sh"
. "$INTEGRATION_TESTS_FOLDER/export.sh"
. "$INTEGRATION_TESTS_FOLDER/search.sh"
. "$INTEGRATION_TESTS_FOLDER/management.sh"
. "$INTEGRATION_TESTS_FOLDER/documentation.sh"
