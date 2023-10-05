import pika


class RabbitMQConsumer:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__userName = "guest"
        self.__password = "guest"
        self.queue = "data_queue"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__userName,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()

        channel.queue_declare(
            queue=self.queue,
            durable=True
        )

        channel.basic_consume(
            queue=self.queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        print(f'Listen RabbitMQ on Port 5672')
        self.__channel.start_consuming()

