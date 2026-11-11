package com.practice.helpdesk.repository;

import com.practice.helpdesk.model.Ticket;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * In-memory "tickets" table that behaves like a real database:
 * it hands out COPIES, so a change is kept only after you call save().
 */
@Repository
public class TicketRepository {

    private final Map<Long, Ticket> table = new ConcurrentHashMap<>();
    private final AtomicLong nextId = new AtomicLong(1);

    public Ticket save(Ticket ticket) {
        if (ticket.getId() == null) {
            ticket.setId(nextId.getAndIncrement());
        }
        table.put(ticket.getId(), ticket.copy());
        return ticket.copy();
    }

    public Optional<Ticket> findById(Long id) {
        Ticket stored = table.get(id);
        return stored == null ? Optional.empty() : Optional.of(stored.copy());
    }

    public List<Ticket> findAll() {
        List<Ticket> result = new ArrayList<>();
        for (Ticket t : table.values()) {
            result.add(t.copy());
        }
        return result;
    }

    public void deleteAll() {
        table.clear();
        nextId.set(1);
    }
}
