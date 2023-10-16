import docker
import os

# Specify the absolute path to your resolution directory
BASE_PATH = ''


def run_containerizer():
    image_tag_name = "temurin-gradlew:17"
    container_name = "executor-container"

    docker_client = docker.from_env()

    # Create Dockerfile, overwriting preexistent
    with open('Dockerfile', 'w') as file:
        file.write(
            '''
            # Use Gradle to build the application
            FROM gradle:7.3.3-jdk17 as build
            WORKDIR /app
            RUN gradle init --type java-library
            COPY resolution/resolutionFile.java /app/src/main/java/com/resolution/resolutionFile
            COPY resolution/testFile.java /app/src/test/java/com/testresolution/testFile
            RUN echo "plugins {" > build.gradle && \
                echo "    id 'java'" >> build.gradle && \
                echo "}" >> build.gradle && \
                echo "repositories {" >> build.gradle && \
                echo "    mavenCentral()" >> build.gradle && \
                echo "}" >> build.gradle && \
                echo "dependencies {" >> build.gradle && \
                echo "    testImplementation 'junit:junit:4.13.2'" >> build.gradle && \
                echo "}" >> build.gradle && \
                echo "test {" >> build.gradle && \
                echo "    useJUnitPlatform()" >> build.gradle && \
                echo "}" >> build.gradle
            RUN gradle build
            
            # Use Java to run the application
            FROM eclipse-temurin:17
            WORKDIR /app
            COPY --from=build /app /app
            RUN apt-get update && apt-get install -y dos2unix
            RUN dos2unix gradlew && chmod +x gradlew
            CMD ["./gradlew", "test"]
   
            '''
        )

    # build an image from the Dockerfile
    temurin_gradlew_image, build_logs = docker_client.images.build(
        path='.',
        dockerfile='Dockerfile',
        tag=image_tag_name,
        rm=True
    )

    # delete the Dockerfile
    if os.path.exists(BASE_PATH + 'Dockerfile'):
        os.remove(BASE_PATH + 'Dockerfile')

    # Create a container from the image
    temurin_container = docker_client.containers.create(
        image=temurin_gradlew_image,
        name=container_name,
        working_dir='/app'
    )

    # Start the container
    temurin_container.start()

    # Create logs
    logs = temurin_container.logs(
        stream=True,
        stderr=True,
        stdout=True,
        timestamps=False,
        tail='all'
    )

    # Print logs
    for log in logs:
        log_line = log.decode().rstrip()
        print(log_line)

    # Stop and remove the container
    temurin_container.stop()
    temurin_container.remove()
