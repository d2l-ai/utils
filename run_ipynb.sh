#!/bin/bash
set -ex

if [ $# -ne 1 ]; then
	echo "Usage: bash $0 NOTEBOOKS"
	echo "E.g., bash run_notebooks.sh 'chap/*'"
	echo "Execute all the notebooks and save outputs (assuming with Python 3)."
	exit -1
fi

NOTEBOOKS=$1

for f in $NOTEBOOKS; do
	echo "==Executing $f"
	jupyter nbconvert --execute --ExecutePreprocessor.kernel_name=python3 --to notebook --inplace $f
done
