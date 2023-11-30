# codeodyssey-executor

### observations:
* it's advised to activate the virtual environment (venv), install dependencies therein and use it to run the application
* if the dependencies are not installed automatically, run `pip install -r requirements.txt`
* Docker is required
* A RabbitMQ service is required 
* with docker, it is possible to create a rabbitMQ service container with `docker run -d --hostname my-rabbit --name codeodyssey-rabbit -p 8085:15672 -p 5672:5672 rabbitmq:3-management` and start it with `docker start codeodyssey-rabbit`
* command to execute the Executor: `python executor.py`
* publish the resolution id on the execution queue and get the message in result queue after the process is finished
* RABBITMQ_HEARTBEAT and RABBITMQ_TTL variables may be changed in order to avoid problems with connection and/or processing, the value of RABBITMQ_TTL must be the same in both api and executor applications
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

