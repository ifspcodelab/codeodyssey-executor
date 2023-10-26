from services.messaging.Consumer import RabbitMQConsumer
from services.messaging.Publisher import RabbitMQPublisher
import threading
from services.containerizer.containerizer import run_containerizer
import base64
import setup
from services.database.database import get_connection_and_cursor
import pika
import time
import psycopg2

result_message = ""
result_message_resolution_id = ""
BASE_PATH = "templates/java/"


def write_to_project(path, extension, file):
    with open(path + '.' + extension, 'w') as fh:
        fh.write(file)


def decode_base64(byte_string):
    return base64.b64decode(byte_string).decode('utf8')


def callback(ch, method, properties, resolution_id):
    t1_callback = time.time()
    connection, cursor = get_connection_and_cursor()
    print(f"Start processing: {resolution_id}")
    id_body = resolution_id.decode('utf8')
    try:
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

        write_to_project(BASE_PATH + 'gradlew-project/src/main/java/com/example/helloworld/hello/world/HelloWorldApplication', extension, resolution_file_dec)
        write_to_project(BASE_PATH + 'gradlew-project/src/test/java/com/example/helloworld/hello/world/HelloWorldApplicationTests', extension, test_file_dec)

        global result_message, result_message_resolution_id
        t1_container = time.time()
        result_message = run_containerizer()
        duration_container = time.time() - t1_container
        result_message_resolution_id = str(id_body)
        publisher = RabbitMQPublisher("executor_exchange", setup.RABBITMQ_ROUTING_KEY, "result_queue")
        publisher.send_message({"id_resolution": result_message_resolution_id, "resolution_message": result_message})
        ch.basic_ack(delivery_tag=method.delivery_tag)
        duration_callback = time.time() - t1_callback
        print(f"Finish processing: {resolution_id} in {duration_callback:.0f}s (container time: {duration_container:.0f}s)")
    except TypeError:
        print(f"TypeError: query with id='{str(id_body)}' returned None")
    except NameError as e:
        print(f"NameError: {e}")
    except pika.exceptions.StreamLostError:
        print("StreamLostError: channel connection closed")
    except psycopg2.errors.InvalidTextRepresentation:
        print("InvalidTextRepresentation: not a uuid")
    cursor.close()
    connection.close()


consumer = RabbitMQConsumer(callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()
