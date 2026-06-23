#!/bin/bash -f

# If CLANG is installed via MacPorts, use it and the gfortran compiler as
# pre-requisites for building SciPy
if command -v port >/dev/null 2>&1 && port -q installed clang-17 >/dev/null 2>&1; then
    echo "Setting up clang from MacPorts"
    export CC=/opt/local/bin/clang-mp-17
    export CXX=/opt/local/bin/clang++-mp-17
    export FC=/opt/local/bin/gfortran-mp-13
    export PKG_CONFIG_PATH=/opt/local/lib/pkgconfig
fi

# Deactivate and remove the old virtual environment, if present
echo "Removing existing Virtual Environment, if present ..."
deactivate 2> /dev/null || true
rm -fr venv

# Create a new environment and activate it
echo "Creating new Virtual Environment ..."
python -m venv venv
. venv/bin/activate

# Make sure pip is up to date
pip install --upgrade pip

# Install the analyser and its direct dependencies
pip install --editable .
