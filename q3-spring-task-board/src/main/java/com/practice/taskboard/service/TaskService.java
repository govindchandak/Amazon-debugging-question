package com.practice.taskboard.service;

import com.practice.taskboard.dto.CreateTaskRequest;
import com.practice.taskboard.model.Task;
import com.practice.taskboard.model.TaskStatus;
import com.practice.taskboard.repository.TaskRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.Comparator;
import java.util.List;

@Service
public class TaskService {

    private final TaskRepository repository;

    public TaskService(TaskRepository repository) {
        this.repository = repository;
    }

    public Task create(CreateTaskRequest request) {
        if (request.title() == null || request.title().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Title is required");
        }
        if (request.priority() == null || request.priority() < 1 || request.priority() > 3) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Priority must be 1, 2 or 3");
        }
        Task task = new Task(null, request.title().trim(), request.priority(), TaskStatus.TODO);
        return repository.save(task);
    }

    public Task updateStatus(Long id, TaskStatus newStatus) {
        Task task = repository.findById(id).get();
        task.setStatus(newStatus);
        return task;
    }

    /** High priority (1) first. Same priority: older task (smaller id) first. */
    public List<Task> list(TaskStatus status) {
        return repository.findAll().stream()
                .filter(task -> status == null || task.getStatus() == status)
                .sorted(Comparator.comparingInt(Task::getPriority).reversed()
                        .thenComparingLong(Task::getId))
                .toList();
    }
}
