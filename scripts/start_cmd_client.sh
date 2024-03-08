#!/usr/bin/env bash

PYTHONPATH=$PYTHONPATH:$(pwd)/redblue_demo
export PYTHONPATH

pkill cmd_client

python3 redblue_demo/test-client/cmd_client.py "$1"
