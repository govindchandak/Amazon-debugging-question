package com.practice.taskboard.repository;

import com.practice.taskboard.model.Task;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Stores tasks in memory, but behaves like a real database:
 * it hands out COPIES, so a change is kept only after you call save().
 */
@Repository
public class TaskRepository {

    private final Map<Long, Task> table = new ConcurrentHashMap<>();
    private final AtomicLong nextId = new AtomicLong(1);

    public Task save(Task task) {
        if (task.getId() == null) {
            task.setId(nextId.getAndIncrement());
        }
        table.put(task.getId(), task.copy());
        return task.copy();
    }

    public Optional<Task> findById(Long id) {
        Task stored = table.get(id);
        return stored == null ? Optional.empty() : Optional.of(stored.copy());
    }

    public List<Task> findAll() {
        List<Task> result = new ArrayList<>();
        for (Task task : table.values()) {
            result.add(task.copy());
        }
        return result;
    }

    public void deleteAll() {
        table.clear();
        nextId.set(1);
    }
}
