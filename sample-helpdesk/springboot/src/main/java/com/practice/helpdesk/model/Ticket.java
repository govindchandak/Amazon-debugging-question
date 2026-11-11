package com.practice.helpdesk.model;

import java.util.ArrayList;
import java.util.List;

public class Ticket {

    public static final List<String> STATUSES = List.of("OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED");

    private Long id;
    private String title;
    private String description;
    private String owner;
    private String status;
    private List<Reply> replies;

    public Ticket(Long id, String title, String description, String owner, String status, List<Reply> replies) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.owner = owner;
        this.status = status;
        this.replies = new ArrayList<>(replies);
    }

    public Ticket copy() {
        return new Ticket(id, title, description, owner, status, replies);
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public String getOwner() { return owner; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public List<Reply> getReplies() { return replies; }
}
