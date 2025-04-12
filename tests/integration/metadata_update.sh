#!/bin/bash -f

echo
echo "Updating metadata '$METADATA' for reference '$REFERENCE'"

TIMESTAMP=$(date)
VALUE="Integration Tests @ $TIMESTAMP @ $METADATA"

# Update the metadata
/bin/bash "$PROJECT_ROOT/run.sh" --set --metadata "$METADATA" --value "$VALUE" --reference "$REFERENCE"

# If this is the reference, we also need to update the reference variable
if [ "$METADATA" == "Reference" ]; then
    REFERENCE="$VALUE"
fi

# Report the updated game information
/bin/bash "$PROJECT_ROOT/run.sh" --info --reference "$REFERENCE" &> "$TEST_RESULTS_FOLDER/info_updated_$METADATA.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/info_updated_$METADATA.txt" info
if [ $? -ne 0 ]; then
    exit 1
fi

# Compare to the original - they should be different
diff "$TEST_RESULTS_FOLDER/info.txt" "$TEST_RESULTS_FOLDER/info_updated_$METADATA.txt" >& /dev/null
if [ $? -eq 0 ]; then
    echo "ERROR: No difference in reported game information after update to metadata '$METADATA' has been applied"
    exit 1
fi

# Look for the updated value - it should be present
grep -i "$VALUE" "$TEST_RESULTS_FOLDER/info_updated_$METADATA.txt" >& /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Updated '$METADATA' value not present in the reported game information"
    exit 1
fi
