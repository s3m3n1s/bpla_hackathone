#!/usr/bin/env python

from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from multiprocessing import Queue
from producer import start_producer, proceed_to_deliver, MODULE_NAME
from consumer import start_consumer
from random import randint
import time
from math import ceil

error_coeff = {
    "battary":      1,
    "camera":       10,
    "connector":    2,
    "lidar":        7,
    "glonas":       12,
    "inertional":   6,
    "gps":          25,
    "sprayer":      30
}

discharge_speed = 0.3 # percent per second

def health_monitor():
    i = 1
    start_time = time.time()

    battary =   {"level": 100, "state": "discharging", "health": 100}
    # camera =    {"state": "OK"}
    # connector = {"state": "OK"}
    # lidar =     {"state": "OK"}
    # glonas =    {"state": "OK"}
    # inertional = {"state": "OK"}
    # gps =       {"state": "OK"}
    sprayer =   {"opened": False, "level": 100}
    while True:
        rnd = randint(1, 100)
        if rnd >= error_coeff['battary']:
            if rnd % 1 == 0:
                battary['level'] = 2
            else:
                battary['health'] = 2
        else:
            t = time.time()
            dch = ceil((t-start_time)*discharge_speed)
            start_time = t
            battary['level'] -= dch
        # rnd = randint(1, 100)
        # camera['state'] = "ERR" if rnd >= error_coeff['camera'] else "OK"
        # rnd = randint(1, 100)
        # connector['state'] = "ERR" if rnd >= error_coeff['connector'] else "OK"
        # rnd = randint(1, 100)
        # lidar['state'] = "ERR" if rnd >= error_coeff['lidar'] else "OK"
        # rnd = randint(1, 100)
        # glonas['state'] = "ERR" if rnd >= error_coeff['glonas'] else "OK"
        # rnd = randint(1, 100)
        # inertional['state'] = "ERR" if rnd >= error_coeff['inertional'] else "OK"
        # rnd = randint(1, 100)
        # gps['state'] = "ERR" if rnd >= error_coeff['gps'] else "OK"
        rnd = randint(1, 100)
        if rnd >= error_coeff['sprayer']:
            if rnd % 1 == 0:
                sprayer['opened'] = not sprayer['opened'] 
            else:
                sprayer['level'] = 0

        data = {
            "battary": battary,
            # "camera": camera,
            # "connector": connector,
            # "lidar": lidar,
            # "glonas": glonas,
            # "inertional": inertional,
            # "gps": gps,
            "sprayer": sprayer
        }

        details = {
            'id': i,
            'deliver_to': 'fly_control',
            'type': 'data',
            'data': data,
            'source': MODULE_NAME, 
        }

        proceed_to_deliver(i, details)
        i += 1
        time.sleep(5)

        


if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['hw_control'])

    requests_queue = Queue()
    start_consumer(args, config)
    start_producer(args, config, requests_queue)

    health_monitor()


