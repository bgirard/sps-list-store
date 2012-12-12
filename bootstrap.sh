#!/bin/bash
set -e

ls google_appengine > /dev/null || {
  echo "Extract the appengine sdk to './google_appengine'"
  exit -1
}
