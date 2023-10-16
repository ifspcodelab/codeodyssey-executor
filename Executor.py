from Queue.Consumer import RabbitMQConsumer
from Queue.Publisher import RabbitMQPublisher
import threading
from Containerizer.containerizer import run_containerizer
import psycopg2
import base64
import setup
import os


connection = psycopg2.connect(
    host=setup.POSTGRES_HOST,
    database=setup.POSTGRES_DATABASE,
    user=setup.POSTGRES_USER,
    password=setup.POSTGRES_PASSWORD,
    port=setup.POSTGRES_PORT
)

cursor = connection.cursor()


def decode_base64(byte_string):
    return base64.b64decode(byte_string).decode('utf8')


def callback(ch, method, properties, body):
    print(f"Iniciando processamento: {body}")
    id_body = body.decode('utf8')
    cursor.execute(
        f"SELECT initial_file, solution_file, test_file, resolution_file, activity_id, extension"
        f" FROM activities, resolutions"
        f" WHERE resolutions.id='{id_body}' and activities.id=resolutions.activity_id"
    )
    connection.commit()
    result = cursor.fetchone()
    initial_file, solution_file, test_file, resolution_file, activity_id, extension = result

    initial_file_dec, solution_file_dec, test_file_dec, resolution_file_dec = map(
        decode_base64, (initial_file, solution_file, test_file, resolution_file)
    )

    with open('gradlew-project/src/main/java/com/example/helloworld/hello/world/HelloWorldApplication.' + extension, 'w') as fh:
        fh.write(resolution_file_dec)

    run_containerizer()

    print(f"Concluído processamento: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    cursor.close()
    connection.close()


consumer = RabbitMQConsumer(callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()

publisher = RabbitMQPublisher("my_second_exchange", setup.RABBITMQ_ROUTING_KEY, "my_second_queue")
publisher.send_message("Hello, world! How are you? I am fine, and you? I hope you are doing okay jabsijbdwe")
