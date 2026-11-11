package com.practice.returns.dto;

public record CreateReturnRequest(Long orderId, String reason) {
}
