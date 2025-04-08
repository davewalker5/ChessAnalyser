#!/bin/bash -f

echo
echo "Performing metadata search for game '$REFERENCE'"
echo "Output will be redirected to text files in '$TEST_RESULTS_FOLDER'"

search_term=$(basename "$PGN_FILE")
/bin/bash "$PROJECT_ROOT/run.sh" --search "$search_term" >& "$TEST_RESULTS_FOLDER/search.txt"
