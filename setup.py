from dotenv import dotenv_values

config = {
    **dotenv_values('.env.shared'),
    **dotenv_values('.env.secret')
}

# Postgres
POSTGRES_HOST = config['POSTGRES_HOST_SECRET'] if getattr(config, 'POSTGRES_HOST_SECRET', None) else config['POSTGRES_HOST']
POSTGRES_PORT = config['POSTGRES_PORT_SECRET'] if getattr(config, 'POSTGRES_PORT_SECRET', None) else config['POSTGRES_PORT']
POSTGRES_DATABASE = config['POSTGRES_DATABASE_SECRET'] if getattr(config, 'POSTGRES_DATABASE_SECRET', None) else config['POSTGRES_DATABASE']
POSTGRES_USER = config['POSTGRES_USER_SECRET'] if getattr(config, 'POSTGRES_USER_SECRET', None) else config['POSTGRES_USER']
POSTGRES_PASSWORD = config['POSTGRES_PASSWORD_SECRET'] if getattr(config, 'POSTGRES_PASSWORD_SECRET', None) else config['POSTGRES_PASSWORD']

# RabbitMQ
RABBITMQ_ROUTING_KEY = config['RABBITMQ_ROUTING_KEY_SECRET'] if getattr(config, 'RABBITMQ_ROUTING_KEY_SECRET', None) else config['RABBITMQ_ROUTING_KEY']
RABBITMQ_USERNAME = config['RABBITMQ_USERNAME_SECRET'] if getattr(config, 'RABBITMQ_USERNAME_SECRET', None) else config['RABBITMQ_USERNAME']
RABBITMQ_PASSWORD = config['RABBITMQ_PASSWORD_SECRET'] if getattr(config, 'RABBITMQ_PASSWORD_SECRET', None) else config['RABBITMQ_PASSWORD']
RABBITMQ_HOST = config['RABBITMQ_HOST_SECRET'] if getattr(config, 'RABBITMQ_HOST_SECRET', None) else config['RABBITMQ_HOST']
RABBITMQ_PORT = config['RABBITMQ_PORT_SECRET'] if getattr(config, 'RABBITMQ_PORT_SECRET', None) else config['RABBITMQ_PORT']
