#!/bin/bash
# Upload files into a github repo.
set -ex

if [ $# -ne 2 ]; then
    echo "ERROR: needs two arguments. "
    echo "Sample usage:"
    echo "   $0 notebooks d2l-ai/notebooks"
    exit -1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IN_DIR="$( cd $1 && pwd )"
REPO=$2
REPO_DIR=${IN_DIR}_git

# clone the repo, make sure GIT_USERNAME and GIT_PASSWORD have already set
rm -rf ${REPO_DIR}
git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/${REPO}.git ${REPO_DIR}

# remove all except for README.md. so we can remove deleted files properly
tmp=$(mktemp)
mv ${REPO_DIR}/README.md $tmp
rm -rf ${REPO_DIR}/*
mv $tmp ${REPO_DIR}/

cp -r ${IN_DIR}/* ${REPO_DIR}

git config --global push.default simple
git add *
git commit -am "Upload"
git push
