package com.practice.helpdesk.auth;

import java.util.Map;

public final class Users {

    public static final Map<String, String> ROLES = Map.of(
            "asha", "CUSTOMER",
            "ravi", "CUSTOMER",
            "neha", "AGENT");

    private Users() {
    }
}
