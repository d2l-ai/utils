#!/bin/bash
# convert all .md files into .ipynb files without evaluation.
set -e

if [ $# -ne 2 ]; then
    echo "ERROR: needs two arguments. "
    echo "Usage:"
    echo "   $0 input_dir output_dir"
    exit -1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IN_DIR="$( cd $1 && pwd )"
# remove out dir contents, in case some files are removed in IN_DIR
rm -rf $2
mkdir $2
OUT_DIR="$( cd $2 && pwd )"

cd ${IN_DIR}

for file in $(find . -not -path "./build/*" -name "*.md"); do
    mkdir -p ${OUT_DIR}/$(dirname $file)
    export EVAL=0; python ${SCRIPT_DIR}/md2ipynb.py ${file} ${OUT_DIR}/${file%.md}.ipynb
done

for file in $(find data img -type f); do
    mkdir -p ${OUT_DIR}/$(dirname $file)
    cp ${file} ${OUT_DIR}/${file}
done
