#!/usr/bin/env bash

PYTHONPATH=$PYTHONPATH:$(pwd)/redblue_demo
export PYTHONPATH

pkill cmd_client
python3 redblue_demo/test-client/test_client.py http://localhost:13000  http://localhost:13001  http://localhost:13002 