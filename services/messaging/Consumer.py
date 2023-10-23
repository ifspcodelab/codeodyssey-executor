import pika
import setup


class RabbitMQConsumer:
    def __init__(self, callback) -> None:
        self.__host = setup.RABBITMQ_HOST
        self.__port = setup.RABBITMQ_PORT
        self.__userName = setup.RABBITMQ_USERNAME
        self.__password = setup.RABBITMQ_PASSWORD
        self.queue = "execution_queue"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__userName,
                password=self.__password
            ),
            heartbeat=60
        )

        channel = pika.BlockingConnection(connection_parameters).channel()

        channel.queue_declare(
            queue=self.queue,
            durable=True
        )

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        print(f'Listen RabbitMQ on Port 5672')
        self.__channel.start_consuming()

