#!/bin/bash -f

echo
echo "Testing console reporting options for game '$REFERENCE'"
echo "Output will be redirected to text files in '$TEST_RESULTS_FOLDER'"

/bin/bash "$PROJECT_ROOT/run.sh" --results --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/results.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/results.txt" results
if [ $? -ne 0 ]; then
    exit 1
fi

/bin/bash "$PROJECT_ROOT/run.sh" --white --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/white.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/white.txt" results
if [ $? -ne 0 ]; then
    exit 1
fi

/bin/bash "$PROJECT_ROOT/run.sh" --black --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/black.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/black.txt" results
if [ $? -ne 0 ]; then
    exit 1
fi

/bin/bash "$PROJECT_ROOT/run.sh" --summary --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/summary.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/summary.txt" summary
if [ $? -ne 0 ]; then
    exit 1
fi

/bin/bash "$PROJECT_ROOT/run.sh" --winchance --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/winchance.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/winchance.txt" winchance
if [ $? -ne 0 ]; then
    exit 1
fi

/bin/bash "$PROJECT_ROOT/run.sh" --info --reference "$REFERENCE" &> "$TEST_RESULTS_FOLDER/info.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/info.txt" info
if [ $? -ne 0 ]; then
    exit 1
fi

/bin/bash "$PROJECT_ROOT/run.sh" --list-metadata &> "$TEST_RESULTS_FOLDER/metadata.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/metadata.txt" metadata
if [ $? -ne 0 ]; then
    exit 1
fi

/bin/bash "$PROJECT_ROOT/run.sh" --players &> "$TEST_RESULTS_FOLDER/players.txt"
/bin/bash "$INTEGRATION_TESTS_FOLDER/verify.sh" "$TEST_RESULTS_FOLDER/players.txt" players
if [ $? -ne 0 ]; then
    exit 1
fi
