package com.practice.taskboard.dto;

import com.practice.taskboard.model.TaskStatus;

public record UpdateStatusRequest(TaskStatus status) {
}
