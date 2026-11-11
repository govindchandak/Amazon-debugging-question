package com.practice.helpdesk.service;

import com.practice.helpdesk.auth.AppUser;
import com.practice.helpdesk.dto.TicketDetail;
import com.practice.helpdesk.dto.TicketSummary;
import com.practice.helpdesk.model.Reply;
import com.practice.helpdesk.model.Ticket;
import com.practice.helpdesk.repository.TicketRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.Comparator;
import java.util.List;

@Service
public class TicketService {

    static final int PAGE_SIZE = 5;

    private final TicketRepository repository;

    public TicketService(TicketRepository repository) {
        this.repository = repository;
    }

    public TicketSummary create(String title, String description, AppUser user) {
        Ticket ticket = new Ticket(null, title, description, user.name(), "OPEN", List.of());
        return TicketSummary.of(repository.save(ticket));
    }

    /** Customers see only their own tickets. Agents see all. Newest first, 5 per page. */
    public List<TicketSummary> list(AppUser user, int page) {
        int start = page * PAGE_SIZE;
        return repository.findAll().stream()
                .filter(t -> user.isAgent() || t.getOwner().equals(user.name()))
                .sorted(Comparator.comparing(Ticket::getId).reversed())
                .skip(start)
                .limit(PAGE_SIZE)
                .map(TicketSummary::of)
                .toList();
    }

    /** Loads a ticket the user is allowed to see. */
    Ticket findVisibleTicket(Long id, AppUser user) {
        Ticket ticket = repository.findById(id).get();
        return ticket;
    }

    public TicketDetail get(Long id, AppUser user) {
        return TicketDetail.of(findVisibleTicket(id, user));
    }

    public Reply addReply(Long id, String message, AppUser user) {
        Ticket ticket = findVisibleTicket(id, user);
        if (message == null || message.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Message is required");
        }
        Reply reply = new Reply(user.name(), message.trim());
        ticket.getReplies().add(reply);
        return reply;
    }

    public TicketSummary changeStatus(Long id, String newStatus, AppUser user) {
        if (!user.isAgent()) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Only agents can change status");
        }
        if (!Ticket.STATUSES.contains(newStatus)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Unknown status");
        }
        Ticket ticket = repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Ticket not found"));
        ticket.setStatus(newStatus);
        return TicketSummary.of(repository.save(ticket));
    }

    /** How many replies on my tickets were written by someone else. */
    public long countRepliesFromOthers(AppUser user) {
        return repository.findAll().stream()
                .filter(t -> t.getOwner().equals(user.name()))
                .mapToLong(t -> t.getReplies().size())
                .sum();
    }
}
