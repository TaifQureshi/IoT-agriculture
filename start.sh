#!/bin/bash

name=${1}
if [[ -z ${name} ]]; then
    echo "start.sh name ..."
    exit 1
fi

nohup python3 run.py "${name}" >> /temp/"${name}".nohup.out;
