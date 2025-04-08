#!/bin/bash -f

echo
echo "Building documentation"

current_folder=$(pwd -P)
cd "$PROJECT_ROOT/docs"
. make_docs.sh
cd $current_folder
