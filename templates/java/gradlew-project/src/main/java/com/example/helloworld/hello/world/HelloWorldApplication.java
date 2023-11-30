package com.example.helloworld.hello.world;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class HelloWorldApplication {

	public static void main(String[] args) {
		SpringApplication.run(HelloWorldApplication.class, args);
	}

	public static String hello() {
		return "Hello World!";
	}

	public static Integer sumTwoIntegers(Integer a, Integer b) {
		return a + b;
	}

	public static Integer multiplicationTwoIntegers(Integer a, Integer b) {
		return a * b;
	}

}
