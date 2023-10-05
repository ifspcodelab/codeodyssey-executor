from Queue.Consumer import RabbitMQConsumer
from Queue.Publisher import RabbitMQPublisher
import threading


def my_callback(ch, method, properties, body):
    print(body)


consumer = RabbitMQConsumer(my_callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()

publisher = RabbitMQPublisher("my_second_exchange", "my_second_key", "my_second_queue")
publisher.send_message("Hello, world! How are you? I am fine, and you? I hope you are doing okay jabsijbdwe")


