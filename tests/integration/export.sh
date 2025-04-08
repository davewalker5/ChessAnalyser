#!/bin/bash -f

echo
echo "Testing data export options for game '$REFERENCE'"
echo "Output will be redirected to files named '$EXPORT_FILE_STEM.*' in '$TEST_RESULTS_FOLDER'"

/bin/bash "$PROJECT_ROOT/run.sh" --export --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" --xlsx "$TEST_RESULTS_FOLDER/$EXPORT_FILE_STEM.xlsx"
/bin/bash "$PROJECT_ROOT/run.sh" --export --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" --docx "$TEST_RESULTS_FOLDER/$EXPORT_FILE_STEM.docx"
/bin/bash "$PROJECT_ROOT/run.sh" --export --reference "$REFERENCE" --engine "$ANALYSIS_ENGINE" --pgn "$TEST_RESULTS_FOLDER/$EXPORT_FILE_STEM.pgn"
/bin/bash "$PROJECT_ROOT/run.sh" --export --reference "$REFERENCE" --image "$TEST_RESULTS_FOLDER/$EXPORT_FILE_STEM-001.png" --halfmoves "*"
/bin/bash "$PROJECT_ROOT/run.sh" --export --reference "$REFERENCE" --image "$TEST_RESULTS_FOLDER/$EXPORT_FILE_STEM-002.png" --halfmoves "2"
/bin/bash "$PROJECT_ROOT/run.sh" --export --reference "$REFERENCE" --movie "$TEST_RESULTS_FOLDER/$EXPORT_FILE_STEM-001.mp4" --duration 0.5
/bin/bash "$PROJECT_ROOT/run.sh" --export --reference "$REFERENCE" --movie "$TEST_RESULTS_FOLDER/$EXPORT_FILE_STEM-002.mp4" --duration 0.5 --engine "$ANALYSIS_ENGINE"
