#!/bin/bash -f

echo
echo "Loading PGN file '$PGN_FILE' with reference '$REFERENCE'"
/bin/bash "$PROJECT_ROOT/run.sh" --load --pgn "$PGN_FILE" --reference "$REFERENCE"
