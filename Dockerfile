
            # Use Gradle to build the application
            FROM gradle:7.3.3-jdk17 as build
            WORKDIR /app
            COPY resolution/ /app/
            RUN echo "plugins {" > build.gradle &&                 echo "    id 'org.springframework.boot' version '2.6.1'" >> build.gradle &&                 echo "    id 'io.spring.dependency-management' version '1.0.11.RELEASE'" >> build.gradle &&                 echo "    id 'java'" >> build.gradle &&                 echo "}" >> build.gradle &&                 echo "group = 'com.example'" >> build.gradle &&                 echo "version = '0.0.1-SNAPSHOT'" >> build.gradle &&                 echo "sourceCompatibility = '17'" >> build.gradle &&                 echo "repositories {" >> build.gradle &&                 echo "    mavenCentral()" >> build.gradle &&                 echo "}" >> build.gradle &&                 echo "dependencies {" >> build.gradle &&                 echo "    implementation 'org.springframework.boot:spring-boot-starter'" >> build.gradle &&                 echo "    testImplementation 'org.springframework.boot:spring-boot-starter-test'" >> build.gradle &&                 echo "}" >> build.gradle &&                 echo "test {" >> build.gradle &&                 echo "    useJUnitPlatform()" >> build.gradle &&                 echo "}" >> build.gradle
            RUN gradle clean build
            
            # Use Java to run the application
            FROM eclipse-temurin:17
            RUN apt-get update && apt-get install -y dos2unix
            WORKDIR /app
            COPY --from=build /app/build/libs/*.jar app.jar
            CMD ["java", "-jar", "app.jar"]


            