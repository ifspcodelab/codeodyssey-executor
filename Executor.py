from Queue.Consumer import RabbitMQConsumer
from Queue.Publisher import RabbitMQPublisher
import threading
import time
from Containerizer.containerizer import run_containerizer


def callback(ch, method, properties, body):
    print(f"Iniciando processamento: {body}")
    run_containerizer()
    print(f"Concluído processamento: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


consumer = RabbitMQConsumer(callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()

publisher = RabbitMQPublisher("my_second_exchange", "my_second_key", "my_second_queue")
publisher.send_message("Hello, world! How are you? I am fine, and you? I hope you are doing okay jabsijbdwe")
