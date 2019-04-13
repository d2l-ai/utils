#!/bin/bash
set -ex

if [ $# -ne 1 ]; then
    echo "Usage: $0 LANG"
    echo "LANG can be en, zh, ..."
    exit -1
fi

D2L_LANG=$1

export CUDA_VISIBLE_DEVICES=$((EXECUTOR_NUMBER+1)),$((EXECUTOR_NUMBER+2))

conda activate d2l-${D2L_LANG}-build
pip list
rm -rf build/_build/
make html
