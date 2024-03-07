#!/usr/bin/env bash

PYTHONPATH=$PYTHONPATH:$(pwd)/redblue_demo
export PYTHONPATH

pkill -f "server_entrypoint.py"
python3 redblue_demo/entrypoints/server_entrypoint.py 0 localhost:13000 localhost:13001 localhost:13002 &
python3 redblue_demo/entrypoints/server_entrypoint.py 1 localhost:13000 localhost:13001 localhost:13002 &
python3 redblue_demo/entrypoints/server_entrypoint.py 2 localhost:13000 localhost:13001 localhost:13002 &
