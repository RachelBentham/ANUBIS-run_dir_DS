#!/bin/bash

echo "Bash version ${BASH_VERSION}"

#masslabels=("0p5" "0p6" "0p7" "0p8" "0p9" "1" "1p1" "1p2" "1p3" "1p4" "1p5")
#decay="CCDY_qqe"

#events=2000
#runnumbers=("2" "3") #"4" "5")

SampleY=$1
#decay=$2
#mass=$1
config_argument=$2

echo "arguments:"
echo "Index: $1"
echo "Config file: $2"

cd /usera/rcb72/neo-set-anubis/db/DarkScalar/

echo "running:"
echo "python selectLLPs_DS.py --config  $config_argument"
python selectLLPs_DS.py --config  $config_argument