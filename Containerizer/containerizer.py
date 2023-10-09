import docker
import os


def run_containerizer():
    project_name = "gradlew-project"
    image_tag_name = "temurin-gradlew:17"
    container_name = "temurin_gradlew"

    docker_client = docker.from_env()

    # Create Dockerfile, overwriting preexistent
    with open('Dockerfile', 'w') as file:
        file.write(
            '''FROM eclipse-temurin:17
            RUN apt-get update && apt-get install -y dos2unix
            RUN mkdir /app
            COPY {project_name} app/{project_name}
            WORKDIR app/{project_name}
            RUN dos2unix gradlew && chmod +x gradlew
            CMD ["./gradlew", "test"]'''.format(project_name=project_name))

    # build an image from the Dockerfile
    temurin_gradlew_image, build_logs = docker_client.images.build(
        path=r'.',
        dockerfile='Dockerfile',
        tag=image_tag_name,
        rm=True
    )

    # delete the Dockerfile
    if os.path.exists('Dockerfile'):
        os.remove('Dockerfile')

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

    for log in logs:
        log_line = log.decode().rstrip()
        print(log_line)

    #temurin_gradlew_container.stop()
    #temurin_gradlew_container.remove()
