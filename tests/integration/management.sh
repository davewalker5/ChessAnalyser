#!/bin/bash -f

echo
echo "Updating metadata for reference '$REFERENCE'"
TIMESTAMP=$(date)
/bin/bash "$PROJECT_ROOT/run.sh" --set --metadata "Event" --value "Integration Tests @ $TIMESTAMP" --reference "$REFERENCE"

# Report the updated game information
/bin/bash "$PROJECT_ROOT/run.sh" --info --reference "$REFERENCE" &> "$TEST_RESULTS_FOLDER/info_updated.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/info_updated.txt" info
if [ $? -ne 0 ]; then
    exit 1
fi

# Compare to the original - they should be different
diff "$TEST_RESULTS_FOLDER/info.txt" "$TEST_RESULTS_FOLDER/info_updated.txt" >& /dev/null
if [ $? -eq 0 ]; then
    exit 1
fi

echo
echo "Deleting analyses and all game data for reference '$REFERENCE'"
/bin/bash "$PROJECT_ROOT/run.sh" --delete --reference "$REFERENCE" <<< "y"
