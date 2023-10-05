import pika

class RabbitMQPublisher:
    def __init__(self, exchange, routing_key, queue) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = exchange
        self.__routing_key = routing_key
        self.__queue = queue
        self.__channel = self.__create_channel()
        self.__create_exchange()
        self.__create_queue()
        self.__bind_queue_to_exchange()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel


    def __create_exchange(self):
        self.__channel.exchange_declare(exchange=self.__exchange, exchange_type='direct')

    def __create_queue(self):
        self.__channel.queue_declare(queue=self.__queue)

    def __bind_queue_to_exchange(self):
        self.__channel.queue_bind(exchange=self.__exchange, queue=self.__queue, routing_key=self.__routing_key)

    def send_message(self, body):
        self.__channel.basic_publish(
            routing_key=self.__routing_key,
            exchange=self.__exchange,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )


rabbitmq_publisher = RabbitMQPublisher("new_exchange", "my_key", "my_queue")
rabbitmq_publisher.send_message("ola, mundo")
