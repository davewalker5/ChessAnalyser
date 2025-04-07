#!/bin/bash -f

# Check the file path and analysis engine have been specified
if (( $# != 2 )); then
    echo Usage: $0 PGN_FILE_ABSOLUTE_PATH ENGINE
    exit 1
fi

# Set the environment
INTEGRATION_TESTS_FOLDER="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PROJECT_ROOT="$INTEGRATION_TESTS_FOLDER/../.."

# Delete and re-create the test results folder to remove pre-existing results, if any
TEST_RESULTS_FOLDER="$PROJECT_ROOT/tests/results"
rm -fr "$TEST_RESULTS_FOLDER"
if [ ! -d "$TEST_RESULTS_FOLDER" ]; then
  mkdir -p "$TEST_RESULTS_FOLDER"
fi

# Set the properties to be used in game import, analysis and reporting
REFERENCE="Integration Tests"
PGN_FILE="$1"
ANALYSIS_ENGINE="$2"
EXPORT_FILE_STEM="integration"

# Perform the tests
. "$INTEGRATION_TESTS_FOLDER/prepare.sh"
. "$INTEGRATION_TESTS_FOLDER/load.sh"
. "$INTEGRATION_TESTS_FOLDER/analyse.sh"
. "$INTEGRATION_TESTS_FOLDER/report.sh"
. "$INTEGRATION_TESTS_FOLDER/export.sh"
. "$INTEGRATION_TESTS_FOLDER/search.sh"
. "$INTEGRATION_TESTS_FOLDER/documentation.sh"
