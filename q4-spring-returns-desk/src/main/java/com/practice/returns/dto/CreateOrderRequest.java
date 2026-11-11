package com.practice.returns.dto;

import java.time.LocalDate;

public record CreateOrderRequest(String customerId, long priceInPaise, String status, LocalDate deliveredOn) {
}
