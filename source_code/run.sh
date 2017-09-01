#!/usr/bin/env bash
taskset -c 50 python run_VB_OBTM.py twitter 0 &
taskset -c 51 python run_VB_OBTM.py twitter 0.1 &
taskset -c 52 python run_VB_OBTM.py twitter 0.2 &
taskset -c 53 python run_VB_OBTM.py twitter 0.3 &
taskset -c 54 python run_VB_OBTM.py twitter 0.4 &
taskset -c 55 python run_VB_OBTM.py twitter 0.5 &
taskset -c 56 python run_VB_OBTM.py twitter 0.6 &
taskset -c 57 python run_VB_OBTM.py twitter 0.7 &
taskset -c 58 python run_VB_OBTM.py twitter 0.8 &
taskset -c 59 python run_VB_OBTM.py twitter 0.9 &
wait
