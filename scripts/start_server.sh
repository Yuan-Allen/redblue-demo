#!/usr/bin/env bash

PYTHONPATH=$PYTHONPATH:$(pwd)/redblue_demo
export PYTHONPATH

python3 redblue_demo/server_entrypoint.py 0 localhost:13000
