#!/bin/bash

python3 run_bot.py >greedy.out &
python3 run_chaser.py >chaser.out &
