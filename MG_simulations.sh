#!/bin/bash

echo "Bash version ${BASH_VERSION}"

#masslabels=("0p5" "0p6" "0p7" "0p8" "0p9" "1" "1p1" "1p2" "1p3" "1p4" "1p5")
#decay="CCDY_qqe"

#events=2000
#runnumbers=("2" "3") #"4" "5")

SampleY=$1
#decay=$2
#mass=$1
jobscript_filepath=$2

echo "arguments:"
echo "Sample number: $1"
echo "Jobscript path: $2"

cd /usera/rcb72/Documents/ANUBIS

echo "Running madgraph on jobscript $jobscript_filepath "
./bin/mg5_aMC $jobscript_filepath
