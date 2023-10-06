import docker
import os

global temurin_gradlew_container
project_name = "gradlew-project"
image_tag_name = "temurin-gradlew:17"
container_name = "temurin_gradlew"

docker_client = docker.from_env()

# Create Dockerfile, overwriting preexistent
with open('.Dockerfile', 'w') as file:
    file.write(
        '''
        FROM eclipse-temurin:17\n
        RUN apt-get update\n
        RUN mkdir /app\n
        COPY {project_name} /app/{project_name}\n
        WORKDIR /app\n
        CMD ["./gradlew", "test"]
    '''.format(project_name=project_name)
    )

# build an image from the Dockerfile
temurin_gradlew_image, build_logs = docker_client.images.build(
    path=r'..',
    dockerfile='.Dockerfile',
    tag=image_tag_name,
    rm=True
)

# delete the Dockerfile
if os.path.exists('./.Dockerfile'):
    os.remove('./.Dockerfile')

# Create a container from the image
temurin_gradlew_container = docker_client.containers.create(
    image=temurin_gradlew_image,
    name=container_name,
    working_dir=f'/app/{project_name}'.format(project_name=project_name)
)

# Start the container
temurin_gradlew_container.start()

# Create logs
logs = temurin_gradlew_container.logs(
    stream=True,
    stderr=True,
    stdout=True,
    timestamps=False,
    tail='all'
)

log_lines = []
for log in logs:
    log_line = log.decode().rstrip()
    print(log_line)

temurin_gradlew_container.stop()
temurin_gradlew_container.remove()

