# implements Kafka topic producer functionality

import multiprocessing
import threading
from confluent_kafka import Producer
import json
import time

_requests_queue: multiprocessing.Queue = None

MODULE_NAME = "connector"
MONITOR_MESSAGE_CHANEL = 'monitor'


def proceed_to_deliver(event_id, details):
    _requests_queue.put(details)


def producer_job(_, config: dict, requests_queue: multiprocessing.Queue):
    producer = Producer(config)

    def delivery_callback(err, msg):
        if err:
            print(f"[{MODULE_NAME}][error] Message failed delivery: {err}")

    while True:
        try:
            event_details = requests_queue.get(block=False)
        except Exception:
            print(f"[{MODULE_NAME}] EMPTY QUEUE")
            time.sleep(2)
            event_details = None
        if event_details:
            print(f"[{MODULE_NAME}] SENDING {event_details}")
            producer.produce(MONITOR_MESSAGE_CHANEL, json.dumps(event_details), str(event_details['id']),
                            callback=delivery_callback
                            )
            # Block until the messages are sent.
            producer.poll(10000)
            producer.flush()
        else:
            print(f"[{MODULE_NAME}] Nothing to send")


def start_producer(args, config: dict, requests_queue: multiprocessing.Queue) -> None:
    global _requests_queue
    _requests_queue = requests_queue
    threading.Thread(target=lambda: producer_job(args, config, requests_queue)).start()