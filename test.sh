#!/bin/bash
set -e
pip install unittest2 -q
python src/test-runner.py $PWD/google_appengine $PWD/src
