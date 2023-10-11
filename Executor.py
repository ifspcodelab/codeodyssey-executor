from Queue.Consumer import RabbitMQConsumer
from Queue.Publisher import RabbitMQPublisher
import threading
from Containerizer.containerizer import run_containerizer
import psycopg2
import base64
import setup


connection = psycopg2.connect(
    host=setup.POSTGRES_HOST,
    database=setup.POSTGRES_DATABASE,
    user=setup.POSTGRES_USER,
    password=setup.POSTGRES_PASSWORD,
    port=setup.POSTGRES_PORT
)

cursor = connection.cursor()


def callback(ch, method, properties, body):
    print(f"Iniciando processamento: {body}")
    id_body = body.decode('utf8')
    cursor.execute(f"SELECT * FROM RESOLUTIONS WHERE id='" + id_body + "'")
    connection.commit()
    result = cursor.fetchone()
    print("result: ", end='')
    print(result)
    print("result[4]: " + result[4])
    print(base64.b64decode(result[4]).decode('utf8'))

    # run_containerizer()
    print(f"Concluído processamento: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    cursor.close()
    connection.close()


consumer = RabbitMQConsumer(callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()

publisher = RabbitMQPublisher("my_second_exchange", setup.RABBITMQ_ROUTING_KEY, "my_second_queue")
publisher.send_message("Hello, world! How are you? I am fine, and you? I hope you are doing okay jabsijbdwe")
