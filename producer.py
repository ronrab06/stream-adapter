import pika
import json

DIRECT_EXCHANGE = 'direct'
MESSAGES_EXCHANGE = 'messages-handler-exchange'
MESSAGES_QUEUE = 'messages-queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

length = input ("Enter the length of the message: ")
message = [int(input(f"Enter a number index {i+1}: ")) for i in range(int(length))]
message_body = json.dumps(message)

channel.exchange_declare(exchange=MESSAGES_EXCHANGE, exchange_type=DIRECT_EXCHANGE)
channel.basic_publish(exchange=MESSAGES_EXCHANGE, routing_key=MESSAGES_QUEUE, body=message_body)

print(f"sent message: {message}")

connection.close()