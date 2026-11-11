package com.practice.returns.model;

public class ReturnRequest {

    private Long id;
    private Long orderId;
    private String customerId;
    private String reason;
    private long refundInPaise;

    public ReturnRequest(Long id, Long orderId, String customerId, String reason, long refundInPaise) {
        this.id = id;
        this.orderId = orderId;
        this.customerId = customerId;
        this.reason = reason;
        this.refundInPaise = refundInPaise;
    }

    public ReturnRequest copy() {
        return new ReturnRequest(id, orderId, customerId, reason, refundInPaise);
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getOrderId() { return orderId; }
    public String getCustomerId() { return customerId; }
    public String getReason() { return reason; }
    public long getRefundInPaise() { return refundInPaise; }
}
