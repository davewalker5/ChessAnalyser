#!/bin/bash -f

echo
echo "Analysing game '$REFERENCE' using '$ANALYSIS_ENGINE' and no console output"
/bin/bash "$PROJECT_ROOT/run.sh" --analyse --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE"

echo
echo "Repeating analysis of game '$REFERENCE' using '$ANALYSIS_ENGINE' with verbose output"
/bin/bash "$PROJECT_ROOT/run.sh" --analyse --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" --verbose
