package com.practice.returns.model;

import java.time.LocalDate;

public class Order {

    private Long id;
    private String customerId;
    private long priceInPaise;
    private String status;       // "SHIPPED", "DELIVERED" or "CANCELLED"
    private LocalDate deliveredOn; // null until delivered

    public Order(Long id, String customerId, long priceInPaise, String status, LocalDate deliveredOn) {
        this.id = id;
        this.customerId = customerId;
        this.priceInPaise = priceInPaise;
        this.status = status;
        this.deliveredOn = deliveredOn;
    }

    public Order copy() {
        return new Order(id, customerId, priceInPaise, status, deliveredOn);
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getCustomerId() { return customerId; }
    public long getPriceInPaise() { return priceInPaise; }
    public String getStatus() { return status; }
    public LocalDate getDeliveredOn() { return deliveredOn; }
}
