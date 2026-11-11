package com.practice.returns.service;

import com.practice.returns.dto.CreateReturnRequest;
import com.practice.returns.model.Order;
import com.practice.returns.model.ReturnRequest;
import com.practice.returns.repository.OrderRepository;
import com.practice.returns.repository.ReturnRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

@Service
public class ReturnService {

    static final int RETURN_WINDOW_DAYS = 30;
    static final int RESTOCKING_FEE_PERCENT = 10;

    private final OrderRepository orders;
    private final ReturnRepository returns;

    public ReturnService(OrderRepository orders, ReturnRepository returns) {
        this.orders = orders;
        this.returns = returns;
    }

    public ReturnRequest createReturn(CreateReturnRequest request) {
        if (request.reason() == null || request.reason().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Reason is required");
        }

        Order order = orders.findById(request.orderId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found"));

        if (order.getStatus().equals("CANCELLED")) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Only delivered orders can be returned");
        }

        long daysSinceDelivery = ChronoUnit.DAYS.between(order.getDeliveredOn(), LocalDate.now());
        if (daysSinceDelivery >= RETURN_WINDOW_DAYS) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Return window has closed");
        }

        if (returns.existsByCustomerId(order.getCustomerId())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "A return already exists for this order");
        }

        long refund = calculateRefund(order.getPriceInPaise(), request.reason());
        ReturnRequest created = new ReturnRequest(null, order.getId(), order.getCustomerId(), request.reason(), refund);
        return returns.save(created);
    }

    /** Damaged items get a full refund. Everything else pays a 10% restocking fee. */
    long calculateRefund(long priceInPaise, String reason) {
        if (reason == "DAMAGED") {
            return priceInPaise;
        }
        long fee = priceInPaise * RESTOCKING_FEE_PERCENT / 100;
        return priceInPaise - fee;
    }

    public List<ReturnRequest> returnsFor(String customerId) {
        return returns.findByCustomerId(customerId);
    }
}
