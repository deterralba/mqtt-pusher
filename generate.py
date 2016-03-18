#!/usr/bin/python

from __future__ import (unicode_literals, absolute_import, division, print_function)

import argparse
import subprocess
import time
from random import randint
import os

# We parse the arguments
#========================#

parser = argparse.ArgumentParser(description='Push datadog statsd formated messages using MQTT')
parser.add_argument('ip', help='IP where to send the messages')
parser.add_argument('-p', '--port', type=int, default=1883, help='port where to send the messages')
parser.add_argument('-t', '--topic',  default='topic', help='metric where to sent the messages')
parser.add_argument('-s', '--sensor', default='temperature', help='type of sensor simulated')
parser.add_argument('-w', '--wait', type=float, default=1, help='time in seconds between two messages')
parser.add_argument('-v', '--verbose', default=False,
        action="store_true", help='verbose mode')

args = parser.parse_args()
if args.verbose:
    print('Parsed args :{}'.format(args))


# We create the payload
#=======================#

# if args.sensor not in sensors:
#     raise ValueError('Invalid parameter sensor: "{}"'.format(sensor))

def get_payload(sensor):

    if sensor == 'temperature':
        metric_name, value = 'temperature', str(randint(5, 40))
    elif sensor == 'pressure':
        metric_name, value = 'pressure', str(randint(900, 1100))
    elif sensor == 'light':
        metric_name, value = 'light', str(randint(0, 100))
    elif sensor == 'humidity':
        metric_name, value = 'humidity', str(randint(0, 100))
    else:
        raise ValueError('Invalid parameter sensor: "{}"'.format(sensor))

    return '{}:{}|g|#sensor:{}'.format(metric_name, value, sensor)


# We send the MQTT message
#==========================#

while True:
    cmd = ['mosquitto_pub', '-h', str(args.ip), '-p', str(args.port), '-t', '"{}"'.format(args.topic),
        '-m', '"{}"'.format(get_payload(args.sensor))]
    if args.verbose:
        cmd.append('-d')

    if args.verbose:
        print('Will send {}'.format(cmd))

    # subprocess doesn't correctly send the cmd. Why? It's a mystery
    # proc = subprocess.Popen(cmd)
    # proc.wait()

    os.popen(' '.join(cmd))
    time.sleep(args.wait)


