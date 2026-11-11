package com.practice.returns.controller;

import com.practice.returns.dto.CreateOrderRequest;
import com.practice.returns.model.Order;
import com.practice.returns.repository.OrderRepository;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** Helper endpoint so you (and the tests) can create orders to return. */
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final OrderRepository orders;

    public OrderController(OrderRepository orders) {
        this.orders = orders;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Order create(@RequestBody CreateOrderRequest request) {
        Order order = new Order(null, request.customerId(), request.priceInPaise(), request.status(), request.deliveredOn());
        return orders.save(order);
    }
}
