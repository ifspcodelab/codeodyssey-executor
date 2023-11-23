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
from services.logging.Logger import Logger


logger = Logger.get_logger_without_handler()

result_message = ""
result_message_resolution_id = ""
BASE_PATH = "templates/java/"


def write_to_project(path, extension, file):
    with open(path + '.' + extension, 'w') as fh:
        fh.write(file)


def decode_base64(byte_string):
    return base64.b64decode(byte_string).decode('utf8')

def count_tries(ch, method, properties, body):
    logger.warning(f"Error processing {body}")

    retries_count = int(properties.headers.get('x-retries-count', 0))
    max_retries = 2

    if retries_count < max_retries:
        properties.headers['x-retries-count'] = retries_count + 1
        try:
            ch.basic_publish(
                exchange='',
                routing_key='execution_queue',
                body=body,
                properties=pika.BasicProperties(
                    headers=properties.headers,
                    delivery_mode=2
                )
            )
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        try:
            logger.info(f"{body} was sent to execution dead letter queue")
            ch.basic_publish(
                exchange='execution_dlx',
                routing_key='execution_dlq_key',
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, resolution_id):
    id_body = resolution_id.decode('utf8')
    logger.info(f"Start processing: {id_body}")
    t1_callback = time.time()
    try:
        connection, cursor = get_connection_and_cursor()
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
        result_message = run_containerizer(id_body)
        duration_container = time.time() - t1_container
        result_message_resolution_id = str(id_body)
        publisher = RabbitMQPublisher("executor_exchange", setup.RABBITMQ_ROUTING_KEY, "result_queue")
        publisher.send_message({"resolution_test_result": result_message})
        ch.basic_ack(delivery_tag=method.delivery_tag)
        duration_callback = time.time() - t1_callback
        logger.info(f"Finish processing: {id_body} in {duration_callback:.0f}s (container time: {duration_container:.0f}s)")
        cursor.close()
        connection.close()
    except TypeError:
        logger.warning(f"TypeError: query with id='{str(id_body)}' returned None")
        count_tries(ch, method, properties, resolution_id)
    except NameError as e:
        logger.warning(f"NameError: {e}")
        count_tries(ch, method, properties, resolution_id)
    except pika.exceptions.StreamLostError:
        logger.warning("StreamLostError: channel connection closed")
        count_tries(ch, method, properties, resolution_id)
    except psycopg2.errors.InvalidTextRepresentation:
        logger.warning("InvalidTextRepresentation: not a uuid")
        count_tries(ch, method, properties, resolution_id)
    except psycopg2.OperationalError:
        logger.warning("OperationalError: error with connection")
        count_tries(ch, method, properties, resolution_id)
    except Exception as e:
        logger.warning(f"Exception: {e}")
        count_tries(ch, method, properties, resolution_id)
    
consumer = RabbitMQConsumer(callback)
consumer_thread = threading.Thread(target=consumer.start)
consumer_thread.start()
