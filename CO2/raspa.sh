#!/bin/bash
if [ -r /opt/crc/Modules/current/init/bash ]; then
        source /opt/crc/Modules/current/init/bash
fi
# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

cd /scratch365/jgonza26/Project_HC/CO2/mofs/Foldername
export HOME="/afs/crc.nd.edu/user/j/jgonza26"
export RASPA_DIR=${HOME}/RASPA/simulations
export DYLD_LIBRARY_PATH=${RASPA_DIR}/lib
export LD_LIBRARY_PATH=${RASPA_DIR}/lib
$RASPA_DIR/bin/simulate -i simulation.input
