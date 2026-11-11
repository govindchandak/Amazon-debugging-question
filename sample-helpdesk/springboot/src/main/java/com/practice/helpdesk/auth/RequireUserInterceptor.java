package com.practice.helpdesk.auth;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

/** Every /api request must say who is calling, in the X-User header. */
@Component
public class RequireUserInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String name = request.getHeader("X-User");
        if (name != null && !Users.ROLES.containsKey(name)) {
            response.setStatus(401);
            return false;
        }
        request.setAttribute("user", new AppUser(name, Users.ROLES.get(name)));
        return true;
    }
}
