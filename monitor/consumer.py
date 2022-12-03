# implements Kafka topic consumer functionality

import datetime
import threading
import time
from confluent_kafka import Consumer, OFFSET_BEGINNING
import json
from policies import check_operation
from producer import proceed_to_deliver
from policies import UNIC_NAME_MONITOR, UNIC_NAME_FLY_CONTROL

log_error_flag = False

SELF_TOPIC = "monitor"


def go_back(event_id):
    m = {
        'id': event_id,
        'deliver_to': 'position',
        'type': 'data',
        'data': '',
        'source': 'central',
    }
    proceed_to_deliver(event_id, m)


def handle_event(event_id, details):
    print(f"[MONITOR][debug] handling event {event_id}, {details}")
    print(f"[MONITOR][info] handling event {event_id}, {details['source']}->{details['deliver_to']}: {details['data']}")
    global log_error_flag
    try:
        text_file = open("/storage/logs.txt", "a+")
        t = time.time()
        text_file.write(f"[{t}] id {event_id}, {details['source']}->{details['deliver_to']}: {details['data']}\n")
    except Exception as e:
        print('[error] log failed')
        if not log_error_flag:
            # go_back(id)
            log_error_flag = True
    text_file.write(details + "\n")

    if check_operation(id, details):
        proceed_to_deliver(id, details)
    else:
        print(f"[error] !!!! policies check failed, delivery unauthorized !!! id:"
                f" {id}, {details['source']}->{details['deliver_to']}: {details['type']} ")
        print(f"[error] suspicious event details: {details}")



def consumer_job(args, config):
    # Create Consumer instance
    monitor_consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_callback(self, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            self.assign(partitions)

    # Subscribe to topic
    monitor_consumer.subscribe([SELF_TOPIC], on_assign=reset_callback)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = monitor_consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("[MONITOR] Waiting...")
                pass
            elif msg.error():
                print(f"[MONITOR] [error] {msg.error()}")
            else:
                # Extract the (optional) key and value, and print.
                try:
                    print(f"[MONITOR] GOT {msg}")
                    event_id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    print("[MONITOR] [debug] consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                        topic=msg.topic(), key=event_id, value=details_str))
                    handle_event(event_id, json.loads(details_str))
                except Exception as e:
                    print(
                        f"[MONITOR] [error] malformed event received from topic {SELF_TOPIC}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        monitor_consumer.close()


def start_consumer(args, config):
    threading.Thread(target=lambda: consumer_job(args, config)).start()
