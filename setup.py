from dotenv import dotenv_values

config = {
    **dotenv_values('.env.shared'),
    **dotenv_values('.env.secret')
}

# Postgres
POSTGRES_HOST = config['POSTGRES_HOST_SECRET'] if config['POSTGRES_HOST_SECRET'] else config['POSTGRES_HOST']
POSTGRES_PORT = config['POSTGRES_PORT_SECRET'] if config['POSTGRES_PORT_SECRET'] else config['POSTGRES_PORT']
POSTGRES_DATABASE = config['POSTGRES_DATABASE_SECRET'] if config['POSTGRES_DATABASE_SECRET'] else config['POSTGRES_DATABASE']
POSTGRES_USER = config['POSTGRES_USER_SECRET'] if config['POSTGRES_USER_SECRET'] else config['POSTGRES_USER']
POSTGRES_PASSWORD = config['POSTGRES_PASSWORD_SECRET'] if config['POSTGRES_PASSWORD_SECRET'] else config['POSTGRES_PASSWORD']

# RabbitMQ
RABBITMQ_ROUTING_KEY = config['RABBITMQ_ROUTING_KEY_SECRET'] if config['RABBITMQ_ROUTING_KEY_SECRET'] else config['RABBITMQ_ROUTING_KEY']