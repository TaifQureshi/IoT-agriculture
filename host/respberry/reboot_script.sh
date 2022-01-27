#!/bin/bash

RUN_PATH='/home/pi/IoT-agriculture/'


# start the client
cd ${RUN_PATH};

nohup python3 run.py raspberrypi;
