#!/bin/bash -f

METADATA="Event"
. "$INTEGRATION_TESTS_FOLDER/metadata_update.sh"

METADATA="White"
. "$INTEGRATION_TESTS_FOLDER/metadata_update.sh"

# Check the reported player list has changed
/bin/bash "$PROJECT_ROOT/run.sh" --players &> "$TEST_RESULTS_FOLDER/players_updated.txt"
diff "$TEST_RESULTS_FOLDER/players.txt" "$TEST_RESULTS_FOLDER/players_updated_white.txt" >& /dev/null
if [ $? -eq 0 ]; then
    echo "ERROR: No difference in reported player list after update to metadata '$METADATA' has been applied"
    exit 1
fi

# Look for the new player - it should be present
grep -i "$VALUE" "$TEST_RESULTS_FOLDER/players_updated.txt" >& /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Player '$VALUE' value not present in the reported player information"
    exit 1
fi

METADATA="Reference"
. "$INTEGRATION_TESTS_FOLDER/metadata_update.sh"

echo
echo "Deleting analyses and all game data for reference '$REFERENCE'"
/bin/bash "$PROJECT_ROOT/run.sh" --delete --reference "$REFERENCE" <<< "y"
