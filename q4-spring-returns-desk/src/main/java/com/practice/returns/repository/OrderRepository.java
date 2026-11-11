package com.practice.returns.repository;

import com.practice.returns.model.Order;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/** In-memory "orders" table. Hands out copies, like a real database. */
@Repository
public class OrderRepository {

    private final Map<Long, Order> table = new ConcurrentHashMap<>();
    private final AtomicLong nextId = new AtomicLong(1);

    public Order save(Order order) {
        if (order.getId() == null) {
            order.setId(nextId.getAndIncrement());
        }
        table.put(order.getId(), order.copy());
        return order.copy();
    }

    public Optional<Order> findById(Long id) {
        Order stored = table.get(id);
        return stored == null ? Optional.empty() : Optional.of(stored.copy());
    }

    public void deleteAll() {
        table.clear();
        nextId.set(1);
    }
}
