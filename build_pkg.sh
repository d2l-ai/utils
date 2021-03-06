#!/bin/bash
set -ex

if [ $# -ne 1 ]; then
    echo "Usage: $0 LANG"
    echo "LANG can be en, zh, ..."
    exit -1
fi

D2L_LANG=$1

# avoid putting data downloaded by scripts into the notebook package
mv build/data build/data-bak
make pkg
# backup build/data to avoid download the dataset each time and put the
rm -rf build/data
mv build/data-bak build/data


if [ $D2L_LANG == zh ]; then
    # For bump version 1.1
    echo "Copying current build to d2l-zh-1.1.zip"
    cp build/_build/html/d2l-${D2L_LANG}.zip build/_build/html/d2l-${D2L_LANG}-1.1.zip
fi

