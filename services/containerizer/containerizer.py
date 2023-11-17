import docker
import os
from .xml_to_json import xml_to_json

BASE_PATH = 'templates/java/'


def run_containerizer():
    try:
        project_name = "gradlew-project"
        image_tag_name = "temurin-gradlew:17"
        container_name = "temurin_gradlew"

        docker_client = docker.from_env()

        # Create Dockerfile, overwriting preexistent
        with open(BASE_PATH + 'Dockerfile', 'w') as file:
            file.write(
                '''FROM eclipse-temurin:17
                RUN apt-get update && apt-get install -y dos2unix
                RUN mkdir /app
                COPY {project_name} app/{project_name}
                WORKDIR app/{project_name}
                RUN dos2unix gradlew && chmod +x gradlew
                CMD ["./gradlew", "test"]'''.format(project_name=project_name, BASE_PATH=BASE_PATH))

        # Clean unused images
        docker_client.images.prune()

        # build an image from the Dockerfile

        temurin_gradlew_image, build_logs = docker_client.images.build(
            path=r'./' + BASE_PATH,
            dockerfile='Dockerfile',
            tag=image_tag_name,
            rm=True
        )

        # delete the Dockerfile and container if exists
        if os.path.exists(BASE_PATH + 'Dockerfile'):
            os.remove(BASE_PATH + 'Dockerfile')

        # Delete a container with the same name, if exists
        # It should not work for more than one container instantiated at the same time, TODO: find a better solution
        for container in docker_client.containers.list(all=True):
            if container.attrs['Name'] == '/' + container_name:
                docker_client.containers.get(container.id).stop()
                docker_client.containers.get(container.id).remove()

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

        # Print logs
        # Couldn't remove this code
        log_lines = ''
        for log in logs:
            log_line = log.decode()
            log_lines += log_line
            # print(log_line)

        command = "cat ./build/test-results/test/TEST-com.example.helloworld.hello.world.HelloWorldApplicationTests.xml"

        if not temurin_gradlew_container.status == 'running':
            temurin_gradlew_container.restart()

        exec_response = temurin_gradlew_container.exec_run(
                cmd=["sh", "-c", command],
                stdout=True,
                stderr=True,
                detach=False,
                tty=True 
            )

        # Stop and remove the container
        temurin_gradlew_container.stop()
        temurin_gradlew_container.remove()

        return xml_to_json(exec_response.output.decode("utf-8"))
    except docker.errors.BuildError:
        print("BuildError: Error building the image")
    except TypeError:
        print("TypeError: error with the path or file object")
    except docker.errors.ImageNotFound:
        print("ImageError: image not found")
    except docker.errors.APIError as e:
        print(f"APIError: {e}")
    except Exception as e:
        print(f"Exception: {e}")