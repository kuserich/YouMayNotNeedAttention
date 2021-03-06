#! /bin/bash

SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

python_location=`which python`

if [[ $python_location == *"/usr/bin"* ]]; then
    echo "Do not run this script without activating a virtual environment first"
    echo "To activate your virtual environment:"
    echo "source ${VENVS_DIR}/${APP_NAME}/bin/activate"
    exit
fi

mkdir -p ${TOOLS_DIR}

# install sockeye for sockeye-autopilot
pip install sockeye

# install Moses scripts for preprocessing
pip install mosestokenizer

# install fast_align
git clone https://github.com/clab/fast_align.git ${TOOLS_DIR}/fast_align
cd ${TOOLS_DIR}/fast_align
cmake .
make
