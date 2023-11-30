import pika
import setup
from services.logging.Logger import Logger


logger = Logger.get_logger()


class RabbitMQConsumer:
    def __init__(self, callback) -> None:
        self.__host = setup.RABBITMQ_HOST
        self.__port = setup.RABBITMQ_PORT
        self.__userName = setup.RABBITMQ_USERNAME
        self.__password = setup.RABBITMQ_PASSWORD
        self.__queue = "execution_queue"
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
            heartbeat=int(setup.RABBITMQ_HEARTBEAT)
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        
        channel.exchange_declare(exchange='api_exchange', exchange_type='direct')
        channel.exchange_declare(exchange='execution_dlx', exchange_type='direct')

        channel.queue_declare(queue=self.__queue, durable=True, arguments={
            'x-message-ttl': int(setup.RABBITMQ_TTL),
            'x-dead-letter-exchange': 'execution_dlx',
            'x-dead-letter-routing-key': "execution_dlq_key",
        })
        channel.queue_declare(queue="execution_dlq", durable=True)

        channel.queue_bind(queue=self.__queue, exchange='api_exchange', routing_key='my_first_key')
        channel.queue_bind(queue='execution_dlq', exchange='execution_dlx', routing_key='execution_dlq_key')

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=self.__queue,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        logger.info(f'Listening RabbitMQ on Port {setup.RABBITMQ_PORT}')
        try:
            self.__channel.start_consuming()
        except pika.exceptions.ConnectionWrongStateError:
            logger.error("ConnectionWrongStateError: channel connection closed")
        except Exception as e:
            logger.error(f"Error: {e}")


