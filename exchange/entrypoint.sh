#!/bin/bash

rabbitmq-server &

sleep 5

python3 create_queues.py

tail -f /dev/null
