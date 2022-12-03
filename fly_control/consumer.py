# implements Kafka topic consumer functionality

from datetime import datetime
import multiprocessing
import random
import threading
import time
from confluent_kafka import Consumer, OFFSET_BEGINNING, MODULE_NAME
import json
from producer import proceed_to_deliver
import base64

_requests_queue: multiprocessing.Queue = None
MESSAGE_CHANEL = MODULE_NAME


def handle_event(event_id, details_str):
    details = json.loads(details_str)
    print(f"[info] handling event {event_id}, {details['source']}->{details['deliver_to']}: {{{details['type']}}} {details['data']}")
    global MODULE_NAME
    try:
        delivery_required = False
        # global x
        # global y
        details['source'] = MODULE_NAME
        
        data = details['data']

        if details['type'] == 'action':
            
            # some code to proseed action data

            # no response 
            delivery_required = False
            #############
            # create response
            # delivery_required = True
            # details['deliver_to'] = # DELIVER TO
            # details['type'] = # "action" OR "data"
            # details['data'] = {}
            
        elif details['type'] == 'data':
            
            # some code to proseed data

            # ### no response 
            delivery_required = False
            #############
            # ### create response
            # delivery_required = True
            # details['deliver_to'] = # DELIVER TO
            # details['type'] = # "action" OR "data"
            # details['data'] = {}
        else:
            print(f"[{MODULE_NAME}] [warning] unknown operation!\n{details}")
        if delivery_required:
            proceed_to_deliver(event_id, details)
    except Exception as e:
        print(f"[{MODULE_NAME}] [error] failed to handle request: {e}")


def consumer_job(args, config):
    assert args is not None
    assert isinstance(config, dict)
    # Create Consumer instance
    consumer_chanel = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_callback(self, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            self.assign(partitions)

    # Subscribe to topic
    topic = MESSAGE_CHANEL
    consumer_chanel.subscribe([topic], on_assign=reset_callback)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer_chanel.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                print(f"[{MODULE_NAME}][error] {msg.error()}")
            else:
                try:
                    event_id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    handle_event(event_id, details_str)
                    msg = json.loads(msg.value())
                except Exception as e:
                    print(f"[{MODULE_NAME}][error] Malformed event received from topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer_chanel.close()


def start_consumer(args, config: dict) -> None:
    threading.Thread(target=lambda: consumer_job(args, config)).start()
