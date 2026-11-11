package com.practice.taskboard.model;

public class Task {

    private Long id;
    private String title;
    private int priority; // 1 = high, 2 = medium, 3 = low
    private TaskStatus status;

    public Task(Long id, String title, int priority, TaskStatus status) {
        this.id = id;
        this.title = title;
        this.priority = priority;
        this.status = status;
    }

    public Task copy() {
        return new Task(id, title, priority, status);
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public int getPriority() { return priority; }
    public void setPriority(int priority) { this.priority = priority; }

    public TaskStatus getStatus() { return status; }
    public void setStatus(TaskStatus status) { this.status = status; }
}
