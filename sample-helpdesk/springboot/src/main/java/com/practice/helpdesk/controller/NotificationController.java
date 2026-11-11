package com.practice.helpdesk.controller;

import com.practice.helpdesk.auth.AppUser;
import com.practice.helpdesk.service.TicketService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/notifications")
public class NotificationController {

    private final TicketService service;

    public NotificationController(TicketService service) {
        this.service = service;
    }

    @GetMapping("/count")
    public Map<String, Long> count(@RequestAttribute("user") AppUser user) {
        return Map.of("count", service.countRepliesFromOthers(user));
    }
}
