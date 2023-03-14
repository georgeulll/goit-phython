import pika

import time

from producer import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def stub_function(text):
    print(f" [x] Received {text}")
    time.sleep(1)


def update_bool(text):
    id_ = text.split(',')[0].split(':')[1]
    contact = Contact.objects(pk=id_)
    contact.update(done=True)


def callback(ch, method, properties, body):
    message = body.decode()
    stub_function(message)
    update_bool(message)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
