package com.practice.helpdesk.dto;

import com.practice.helpdesk.model.Reply;
import com.practice.helpdesk.model.Ticket;

import java.util.List;

public record TicketDetail(Long id, String title, String owner, String status, String description, List<Reply> replies) {

    public static TicketDetail of(Ticket t) {
        return new TicketDetail(t.getId(), t.getTitle(), t.getOwner(), t.getStatus(), t.getDescription(), t.getReplies());
    }
}
