#!/usr/bin/env bash

BASE_DIR="/home/grid/users/plgblueeyedhush/sao/"
SCRIPT_DIR="$BASE_DIR/superc/wcss/"

# load required modules
module load plgrid/tools/python/2.7.8

pushd ~/sao

PACKAGES_PREFIX=`readlink -f ~/.python/`/
PACKAGES_PATH="$PACKAGES_PREFIX"/lib/python2.7/site-packages
mkdir -p "$PACKAGES_PATH"
export PYTHONPATH="$PYTHONPATH":"$PACKAGES_PATH"
easy_install --prefix="$PACKAGES_PREFIX" `cat requirements/computation.txt`

python "$BASE_DIR"/evaluate.py

popd