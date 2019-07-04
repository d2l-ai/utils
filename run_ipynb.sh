#!/bin/bash
set -ex

if [ $# -ne 1 ]; then
	echo "Usage: $0 PATH_TO_NOTEBOOKS"
	echo "Execute all the notebooks and save outputs (assuming with Python 3)."
	exit -1
fi

PATH_TO_NOTEBOOKS=$1

for f in $PATH_TO_NOTEBOOKS; do
	echo "==Executing $f"
	jupyter nbconvert --execute --ExecutePreprocessor.kernel_name=python3 --to notebook --inplace $f
done

