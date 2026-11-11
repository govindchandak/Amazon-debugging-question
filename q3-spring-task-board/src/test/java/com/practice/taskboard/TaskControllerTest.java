package com.practice.taskboard;

import com.practice.taskboard.repository.TaskRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class TaskControllerTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private TaskRepository repository;

    @BeforeEach
    void cleanDatabase() {
        repository.deleteAll();
    }

    private ResultActions createTask(String title, int priority) throws Exception {
        String body = "{\"title\": \"" + title + "\", \"priority\": " + priority + "}";
        return mvc.perform(post("/api/tasks").contentType(MediaType.APPLICATION_JSON).content(body));
    }

    private ResultActions changeStatus(long id, String newStatus) throws Exception {
        String body = "{\"status\": \"" + newStatus + "\"}";
        return mvc.perform(patch("/api/tasks/" + id + "/status").contentType(MediaType.APPLICATION_JSON).content(body));
    }

    @Test
    void createTask_returns201_withStatusTodo() throws Exception {
        createTask("Write unit tests", 2)
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.status").value("TODO"));
    }

    @Test
    void createTask_withBlankTitle_returns400() throws Exception {
        createTask("   ", 2).andExpect(status().isBadRequest());
    }

    @Test
    void changeStatus_isSaved() throws Exception {
        createTask("Fix login page", 1);
        changeStatus(1, "DONE").andExpect(status().isOk());

        mvc.perform(get("/api/tasks").param("status", "DONE"))
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].title").value("Fix login page"));
    }

    @Test
    void changeStatus_ofUnknownTask_returns404() throws Exception {
        changeStatus(99, "DONE").andExpect(status().isNotFound());
    }

    @Test
    void list_showsHighPriorityFirst() throws Exception {
        createTask("Update README", 3);
        createTask("Fix payment bug", 1);
        createTask("Review PR", 2);

        mvc.perform(get("/api/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].title").value("Fix payment bug"))
                .andExpect(jsonPath("$[1].title").value("Review PR"))
                .andExpect(jsonPath("$[2].title").value("Update README"));
    }

    @Test
    void list_filtersByStatus() throws Exception {
        createTask("Task A", 1);
        createTask("Task B", 2);

        mvc.perform(get("/api/tasks").param("status", "TODO")).andExpect(jsonPath("$", hasSize(2)));
        mvc.perform(get("/api/tasks").param("status", "DONE")).andExpect(jsonPath("$", hasSize(0)));
    }
}
