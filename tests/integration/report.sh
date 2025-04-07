#!/bin/bash -f

echo
echo "Testing console reporting options for game '$REFERENCE'"
echo "Output will be redirected to text files in '$TEST_RESULTS_FOLDER'"

/bin/bash "$PROJECT_ROOT/run.sh" --results --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/results.txt"
/bin/bash "$PROJECT_ROOT/run.sh" --white --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/white.txt"
/bin/bash "$PROJECT_ROOT/run.sh" --black --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/black.txt"
/bin/bash "$PROJECT_ROOT/run.sh" --summary --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/summary.txt"
/bin/bash "$PROJECT_ROOT/run.sh" --winchance --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" &> "$TEST_RESULTS_FOLDER/winchance.txt"
/bin/bash "$PROJECT_ROOT/run.sh" --info --reference "$REFERENCE" &> "$TEST_RESULTS_FOLDER/info.txt"
