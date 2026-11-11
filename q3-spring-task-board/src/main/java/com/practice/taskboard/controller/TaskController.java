package com.practice.taskboard.controller;

import com.practice.taskboard.dto.CreateTaskRequest;
import com.practice.taskboard.dto.UpdateStatusRequest;
import com.practice.taskboard.model.Task;
import com.practice.taskboard.model.TaskStatus;
import com.practice.taskboard.service.TaskService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    private final TaskService service;

    public TaskController(TaskService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Task create(@RequestBody CreateTaskRequest request) {
        return service.create(request);
    }

    @PatchMapping("/{id}/status")
    public Task updateStatus(@PathVariable("id") Long id, @RequestBody UpdateStatusRequest request) {
        return service.updateStatus(id, request.status());
    }

    @GetMapping
    public List<Task> list(@RequestParam(name = "status", required = false) TaskStatus status) {
        return service.list(status);
    }
}
