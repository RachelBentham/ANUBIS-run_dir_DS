#!/bin/bash

echo "Bash version ${BASH_VERSION}"

#masslabels=("0p5" "0p6" "0p7" "0p8" "0p9" "1" "1p1" "1p2" "1p3" "1p4" "1p5")
#decay="CCDY_qqe"

#events=2000
#runnumbers=("2" "3") #"4" "5")

runID=$1
#decay=$2
#mass=$1
config_argument=$2

echo "arguments:"
echo "runID: $runID"
echo "Config file: $config_argument"

cd /usera/rcb72/neo-set-anubis/db/DarkScalar/

echo "running:"
echo "python select_DS.py --runID $runID --config  $config_argument"
python select_DS.py --runID $runID --config  $config_argument