#!/bin/bash
set -ex

if [ $# -ne 1 ]; then
    echo "Usage: $0 LANG"
    echo "LANG can be en, zh, ..."
    exit -1
fi

LANG=$1

conda activate d2l-${LANG}-build

build/utils/upload_doc_s3.sh build/_build/html s3://${LANG}.d2l.ai
