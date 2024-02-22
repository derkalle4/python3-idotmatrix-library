#!/bin/sh
# install wheel if not done already
pip install wheel
# delete old dist packages if any
rm -rf ./dist/*
# build new packages if any
python setup.py bdist_wheel --universal
