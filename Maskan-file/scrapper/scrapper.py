import pika
import json
import time

def rabbit_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='detector_queue')
    while True:
        # method_frame: metadata about the message (e.g., delivery tag, etc.) (is None if there aren't any messages received)
        #
        # header_frame: headers and properties (Not needed here)
        #
        # body: the actual message you sent from the detector
        method_frame, header_frame, body = channel.basic_get(queue='detector_queue', auto_ack=True)
        if (method_frame):
            data = json.loads(body)
            example_process(data)
        else:
            time.sleep(2)

def example_process(data):
    print(*data, sep="\n")
    print("////////////////////////////////////")
    print("END OF THIS PROCESS")
    print("////////////////////////////////////")
if __name__ == '__main__':
    rabbit_consume()