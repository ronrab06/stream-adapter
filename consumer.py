import pika
import json
from stream_adapter import StreamAdapter

DIRECT_EXCHANGE = 'direct'
MESSAGES_EXCHANGE = 'messages-handler-exchange'
MESSAGES_QUEUE = 'messages-queue'
CHUNKS_EXCHANGE = 'chunks-exchange'
CHUNKS_QUEUE = 'chunks-queue'
MESSAGE_SIZE = 12

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

adapter = StreamAdapter(MESSAGE_SIZE)
channel.exchange_declare(exchange=CHUNKS_EXCHANGE, exchange_type=DIRECT_EXCHANGE)

def handle_message(message):
    chunks = adapter.get_stream_chunks(message)
    message_body = json.dumps(chunks)

    channel.basic_publish(exchange=CHUNKS_EXCHANGE, routing_key=CHUNKS_QUEUE, body=message_body)
    print(f"sent chunks: {chunks}")

def receive_message_callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"received message: {message}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

    handle_message(message)

channel.exchange_declare(exchange=MESSAGES_EXCHANGE, exchange_type=DIRECT_EXCHANGE)
channel.queue_declare(queue=MESSAGES_QUEUE)
channel.queue_bind(exchange=MESSAGES_EXCHANGE, queue=MESSAGES_QUEUE, routing_key=MESSAGES_QUEUE)

channel.basic_consume(queue=MESSAGES_QUEUE, on_message_callback=receive_message_callback, auto_ack=False)

print("listening for messages...")
channel.start_consuming()