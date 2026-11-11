package com.practice.helpdesk.controller;

import com.practice.helpdesk.auth.AppUser;
import com.practice.helpdesk.dto.CreateTicketRequest;
import com.practice.helpdesk.dto.ReplyRequest;
import com.practice.helpdesk.dto.StatusRequest;
import com.practice.helpdesk.dto.TicketDetail;
import com.practice.helpdesk.dto.TicketSummary;
import com.practice.helpdesk.model.Reply;
import com.practice.helpdesk.service.TicketService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestAttribute;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@RestController
@RequestMapping("/api/tickets")
public class TicketController {

    private final TicketService service;

    public TicketController(TicketService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public TicketSummary create(@RequestBody CreateTicketRequest request, @RequestAttribute("user") AppUser user) {
        if (request.title() == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Title is required");
        }
        String description = request.description() == null ? "" : request.description();
        return service.create(request.title().trim(), description, user);
    }

    @GetMapping
    public List<TicketSummary> list(@RequestParam(name = "page", defaultValue = "1") int page,
                                    @RequestAttribute("user") AppUser user) {
        return service.list(user, page);
    }

    @GetMapping("/{id}")
    public TicketDetail get(@PathVariable("id") Long id, @RequestAttribute("user") AppUser user) {
        return service.get(id, user);
    }

    @PostMapping("/{id}/reply")
    @ResponseStatus(HttpStatus.CREATED)
    public Reply addReply(@PathVariable("id") Long id, @RequestBody ReplyRequest request,
                          @RequestAttribute("user") AppUser user) {
        return service.addReply(id, request.message(), user);
    }

    @PatchMapping("/{id}/status")
    public TicketSummary changeStatus(@PathVariable("id") Long id, @RequestBody StatusRequest request,
                                      @RequestAttribute("user") AppUser user) {
        return service.changeStatus(id, request.status(), user);
    }
}
