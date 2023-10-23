from services.messaging.Consumer import RabbitMQConsumer
from services.messaging.Publisher import RabbitMQPublisher
import threading
from services.containerizer.containerizer import run_containerizer
import base64
import setup
from services.database.database import get_connection_and_cursor

result_message = ""
result_message_resolution_id = ""


def write_to_project(path, extension, file):
    with open(path + extension, 'w') as fh:
        fh.write(file)


def decode_base64(byte_string):
    return base64.b64decode(byte_string).decode('utf8')


def callback(ch, method, properties, resolution_id):
    connection, cursor = get_connection_and_cursor()
    print(f"Start processing: {resolution_id}")
    id_body = resolution_id.decode('utf8')
    cursor.execute(
        f"SELECT initial_file, solution_file, test_file, resolution_file, activity_id, extension"
        f" FROM activities, resolutions"
        f" WHERE resolutions.id='{id_body}' and activities.id=resolutions.activity_id"
    )
    connection.commit()
    result = cursor.fetchone()
    try:
        initial_file, solution_file, test_file, resolution_file, activity_id, extension = result
        initial_file_dec, solution_file_dec, test_file_dec, resolution_file_dec = map(
            decode_base64, (initial_file, solution_file, test_file, resolution_file)
        )

        write_to_project('gradlew-project/src/main/java/com/example/helloworld/hello/world/HelloWorldApplication.', extension, resolution_file_dec)
        write_to_project('gradlew-project/src/test/java/com/example/helloworld/hello/world/HelloWorldApplicationTests.', extension, test_file_dec)

        global result_message, result_message_resolution_id, publisher
        result_message = run_containerizer()
        result_message_resolution_id = str(id_body)
        publisher.send_message({"id_resolution": result_message_resolution_id, "resolution_message": result_message})
    except TypeError:
        print(f"TypeError: query with id='{str(id_body)}' returned None")
    except NameError:
        print(f"NameError: error with message")

    print(f"Finish processing: {resolution_id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    cursor.close()
    connection.close()


consumer = RabbitMQConsumer(callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()

publisher = RabbitMQPublisher("executor_exchange", setup.RABBITMQ_ROUTING_KEY, "result_queue")
