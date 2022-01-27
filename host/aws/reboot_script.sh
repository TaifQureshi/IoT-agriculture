#!/bin/bash

RUN_PATH='/home/ubuntu/IoT-agriculture'


# start the client
cd ${RUN_PATH};

nohup python3 run.py server;
