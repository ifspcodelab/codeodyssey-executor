import base64

from Queue.Consumer import RabbitMQConsumer
from Queue.Publisher import RabbitMQPublisher
import threading
from Containerizer.containerizer import run_containerizer
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres",
    port="5432"
)

cursor = connection.cursor()


def callback(ch, method, properties, body):
    print(f"Iniciando processamento: {body}")

    id_resolution = body

    cursor.execute("""
        SELECT 
            resolutionFile, testFile, extension
        FROM
            RESOLUTION, ACTIVITY
        WHERE
            RESOLUTION.idActivity = ACTIVITY.id AND RESOLUTION.id = %s 
    """, (id_resolution,))

    result = cursor.fetchone()

    resolution_file_bytes = bytes.fromhex(result[0][2:])
    test_file_bytes = bytes.fromhex(result[1][2:])

    decoded_resolution_file_str = base64.b64decode(resolution_file_bytes.decode('utf-8')).decode('utf-8')
    decoded_test_file_str = base64.b64decode(test_file_bytes.decode('utf-8')).decode('utf-8')

    with open(f'resolutionFile.{result[2]}', 'w') as f:
        f.write(decoded_resolution_file_str)

    with open(f'testFile.{result[2]}', 'w') as f:
        f.write(decoded_test_file_str)

    run_containerizer()

    print(f"Concluído processamento: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


consumer = RabbitMQConsumer(callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()

publisher = RabbitMQPublisher("my_second_exchange", "my_second_key", "my_second_queue")
publisher.send_message("Hello, world! How are you? I am fine, and you? I hope you are doing okay jabsijbdwe")
