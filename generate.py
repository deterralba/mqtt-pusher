#!/usr/bin/python

from __future__ import (unicode_literals, absolute_import, division, print_function)

import argparse
import subprocess
import time
from random import randint
import os
import sensor

# We parse the arguments
#========================#

parser = argparse.ArgumentParser(description='Push datadog statsd formated messages using MQTT')
parser.add_argument('ip', help='IP where to send the messages')
parser.add_argument('-p', '--port', type=int, default=1883, help='port where to send the messages')
parser.add_argument('-t', '--topic',  default='topic', help='metric where to sent the messages')
parser.add_argument('-s', '--sensor', default='temperature', help='type of sensor simulated')
parser.add_argument('-w', '--wait', type=float, default=30, help='time in seconds between two messages')
parser.add_argument('--tags', default=None, help='tags sent within the metric messages')
parser.add_argument('-v', '--verbose', default=False,
        action="store_true", help='verbose mode')

args = parser.parse_args()
if args.verbose:
    print('Parsed args :{}'.format(args))


# We create the payload
#=======================#

sensors = {'temperature':sensor.Temperature,
           'pressure':sensor.Pressure,
           'light':sensor.Light,
           'memory':sensor.Memory,
           }
try:
    the_sensor = sensors[args.sensor](tags=args.tags)
except Exception:
    raise ValueError('Wrong paremeters --sensor given: {}'.format(args.sensor))

# We send the MQTT message
#==========================#

while True:
    cmd = ['mosquitto_pub', '-h', str(args.ip), '-p', str(args.port), '-t', '"{}"'.format(args.topic),
        '-m', '"{}"'.format(sensor.get_payload(the_sensor))]
    if args.verbose:
        cmd.append('-d')
    cmd = ' '.join(cmd)

    if args.verbose:
        print('Will execute: {}'.format(cmd))

    # subprocess doesn't correctly send the cmd. Why? It's a mystery
    # proc = subprocess.Popen(cmd)
    # proc.wait()

    os.popen(cmd)
    time.sleep(args.wait)


