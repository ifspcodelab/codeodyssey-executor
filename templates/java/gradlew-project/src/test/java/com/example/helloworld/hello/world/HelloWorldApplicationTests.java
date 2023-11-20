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
	void twoIsEven() {
		Assertions.assertEquals(0, 2%2);
	}

	@Test
	void threeIsOdd() {
		Assertions.assertEquals(0, 3%2);
	}

}