package com.practice.helpdesk.dto;

import com.practice.helpdesk.model.Ticket;

public record TicketSummary(Long id, String title, String owner, String status) {

    public static TicketSummary of(Ticket t) {
        return new TicketSummary(t.getId(), t.getTitle(), t.getOwner(), t.getStatus());
    }
}
