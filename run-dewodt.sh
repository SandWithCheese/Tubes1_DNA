#!/bin/bash

python3 main.py --logic DewoDT --email=testdewodt@email.com --name=dewodt --password=123456 --team etimo &
python3 main.py --logic Sandwich --email=test1@email.com --name=stima1 --password=123456 --team etimo &
python3 main.py --logic Greedy --email=test2@email.com --name=stima2 --password=123456 --team etimo &
python3 main.py --logic Random --email=test3@email.com --name=stima3 --password=123456 --team etimo &