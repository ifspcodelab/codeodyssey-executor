package com.example.helloworld.hello.world;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;


@SpringBootTest
class HelloWorldApplicationTests {

	@Test
	void contextLoads() {
	}

	@Test
	void helloShouldReturnHelloMessage() {
		String helloMessage = HelloWorldApplication.hello();
		Assertions.assertEquals(helloMessage, "Hello World!");
	}

	@Test
	void sumOfTwoAndThreeShouldReturnFive() {
		Integer a = 2;
		Integer b = 3;

		Integer result = HelloWorldApplication.sumTwoIntegers(a, b);

		Assertions.assertEquals(5, result);
	}

	@Test
	void multiplicationOfTwoAndThreeShouldReturnSix() {
		Integer a = 2;
		Integer b = 3;

		Integer result = HelloWorldApplication.multiplicationTwoIntegers(a, b);

		Assertions.assertEquals(6, result);
	}

}