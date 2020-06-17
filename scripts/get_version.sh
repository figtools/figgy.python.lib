#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cat "$SCRIPTPATH/../src/setup.py"| grep -E "VERSION\s+=\s+" | sed -E "s#.*([0-9]+.[0-9]+.[0-9]+[a-zA-Z]?).*#\1#g"