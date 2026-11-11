package com.practice.helpdesk.config;

import com.practice.helpdesk.auth.RequireUserInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    private final RequireUserInterceptor requireUser;

    public WebConfig(RequireUserInterceptor requireUser) {
        this.requireUser = requireUser;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(requireUser).addPathPatterns("/api/**");
    }
}
