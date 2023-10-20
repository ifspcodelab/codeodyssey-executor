import psycopg2
import setup


def get_connection_and_cursor():
    connection = psycopg2.connect(
        host=setup.POSTGRES_HOST,
        database=setup.POSTGRES_DATABASE,
        user=setup.POSTGRES_USER,
        password=setup.POSTGRES_PASSWORD,
        port=setup.POSTGRES_PORT
    )
    cursor = connection.cursor()
    return connection, cursor
