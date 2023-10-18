# codeodyssey-executor

### observations:
* is advised to activate the virtual environment (venv)
* if the dependencies are not installed automatically, run `pip install -r requirements.txt` to install in current directory
* it is necessary to use a rabbitMQ service
* with docker, it is possible to create a rabbitMQ service container with `docker run -d --hostname my-rabbit --name some-rabbit -p 8085:15672 -p 5672:5672 rabbitmq:3-management`
* command to execute the Executor: `python executor.py`
* to hide services credentials, create a file named `.env.secret` in the root directory with the following variables filled out:

```
POSTGRES_HOST_SECRET=
POSTGRES_PORT_SECRET=
POSTGRES_DATABASE_SECRET=
POSTGRES_USER_SECRET=
POSTGRES_PASSWORD_SECRET=


RABBITMQ_ROUTING_KEY_SECRET=
RABBITMQ_USERNAME_SECRET=
RABBITMQ_PASSWORD_SECRET=
RABBITMQ_HOST_SECRET=
RABBITMQ_PORT_SECRET=

```

