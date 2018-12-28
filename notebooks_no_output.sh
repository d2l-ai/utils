#!/bin/bash
# convert all .md files into .ipynb files without evaluation.
set -e

if [ $# -ne 4 ]; then
    echo "ERROR: needs two arguments. "
    echo "Usage:"
    echo "   $0 input_dir output_dir output_github_repo discuss_url"
    exit -1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IN_DIR="$( cd $1 && pwd )"
# remove out dir contents, in case some files are removed in IN_DIR
rm -rf $2
mkdir $2
OUT_DIR="$( cd $2 && pwd )"
GITHUG_REPO=$3
DISCUSS_URL=$4

cd ${IN_DIR}

for file in $(find . -not -path "./build/*" -name "*.md"); do
    mkdir -p ${OUT_DIR}/$(dirname $file)
    python ${SCRIPT_DIR}/md2colab.py ${file} ${OUT_DIR}/${file%.md}.ipynb ${GITHUG_REPO} ${DISCUSS_URL}
done

for file in $(find data img -type f); do
    mkdir -p ${OUT_DIR}/$(dirname $file)
    cp ${file} ${OUT_DIR}/${file}
done

for file in $(find ${OUT_DIR}/img -name "*.svg"); do
    png=${file%.svg}.png
    rsvg-convert -z 4 $file -o $png
    rm -rf $file
done
