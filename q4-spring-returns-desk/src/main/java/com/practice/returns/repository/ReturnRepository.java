package com.practice.returns.repository;

import com.practice.returns.model.ReturnRequest;
import org.springframework.stereotype.Repository;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/** In-memory "returns" table. Hands out copies, like a real database. */
@Repository
public class ReturnRepository {

    private final Map<Long, ReturnRequest> table = new ConcurrentHashMap<>();
    private final AtomicLong nextId = new AtomicLong(1);

    public ReturnRequest save(ReturnRequest request) {
        if (request.getId() == null) {
            request.setId(nextId.getAndIncrement());
        }
        table.put(request.getId(), request.copy());
        return request.copy();
    }

    public boolean existsByOrderId(Long orderId) {
        return table.values().stream().anyMatch(r -> r.getOrderId().equals(orderId));
    }

    public boolean existsByCustomerId(String customerId) {
        return table.values().stream().anyMatch(r -> r.getCustomerId().equals(customerId));
    }

    public List<ReturnRequest> findByCustomerId(String customerId) {
        return table.values().stream()
                .filter(r -> r.getCustomerId().equals(customerId))
                .sorted(Comparator.comparingLong(ReturnRequest::getId))
                .map(ReturnRequest::copy)
                .toList();
    }

    public void deleteAll() {
        table.clear();
        nextId.set(1);
    }
}
