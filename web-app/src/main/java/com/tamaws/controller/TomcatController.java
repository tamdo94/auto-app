package com.tamaws.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collection;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import com.tamaws.controller.VeryLargeObject;

@RestController
public class TomcatController {

    @GetMapping("/hello")
    public Collection<String> sayHello() {

        VeryLargeObject[] vla = new VeryLargeObject[1 << 12];
        for(int i = 0; i < Integer.MAX_VALUE; ++i) {
            vla[i] = new VeryLargeObject("aa");
        }

        return IntStream.range(0, 10)
                .mapToObj(i -> "Hello number " + i)
                .collect(Collectors.toList());
    }

    @GetMapping("/hello2")
    public Collection<String> sayHello2() {

        return IntStream.range(0, 10)
                .mapToObj(i -> "Hello number " + i)
                .collect(Collectors.toList());
    }
}