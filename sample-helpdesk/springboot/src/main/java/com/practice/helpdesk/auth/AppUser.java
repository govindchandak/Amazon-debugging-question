package com.practice.helpdesk.auth;

public record AppUser(String name, String role) {

    public boolean isAgent() {
        return "AGENT".equals(role);
    }
}
