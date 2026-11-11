package com.practice.returns.controller;

import com.practice.returns.dto.CreateReturnRequest;
import com.practice.returns.model.ReturnRequest;
import com.practice.returns.service.ReturnService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/returns")
public class ReturnController {

    private final ReturnService service;

    public ReturnController(ReturnService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ReturnRequest create(@RequestBody CreateReturnRequest request) {
        return service.createReturn(request);
    }

    @GetMapping
    public List<ReturnRequest> list(@RequestParam(name = "customerId") String customerId) {
        return service.returnsFor(customerId);
    }
}
