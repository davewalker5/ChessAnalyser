#!/bin/bash -f

echo
echo "Deleting analyses and all game data for reference '$REFERENCE'"
/bin/bash "$PROJECT_ROOT/run.sh" --delete --reference "$REFERENCE" <<< "y"
