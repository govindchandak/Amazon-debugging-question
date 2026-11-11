package com.practice.helpdesk;

import com.practice.helpdesk.model.Reply;
import com.practice.helpdesk.model.Ticket;
import com.practice.helpdesk.repository.TicketRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

import java.util.List;

import static org.hamcrest.Matchers.contains;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class HelpDeskTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private TicketRepository repository;

    @BeforeEach
    void cleanDatabase() {
        repository.deleteAll();
    }

    private ResultActions send(MockHttpServletRequestBuilder request, String user, String json) throws Exception {
        if (user != null) {
            request.header("X-User", user);
        }
        if (json != null) {
            request.contentType(MediaType.APPLICATION_JSON).content(json);
        }
        return mvc.perform(request);
    }

    private void createTicket(String user, String title) throws Exception {
        send(post("/api/tickets"), user, "{\"title\": \"" + title + "\", \"description\": \"Details\"}")
                .andExpect(status().isCreated());
    }

    // ---------- who is calling ----------

    @Test
    void requestWithoutUserHeader_returns401() throws Exception {
        send(get("/api/tickets"), null, null).andExpect(status().isUnauthorized());
    }

    @Test
    void unknownUser_returns401() throws Exception {
        send(get("/api/tickets"), "hacker", null).andExpect(status().isUnauthorized());
    }

    // ---------- create ticket ----------

    @Test
    void createTicket_returns201_withStatusOpen() throws Exception {
        send(post("/api/tickets"), "asha", "{\"title\": \"Refund missing\"}")
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.owner").value("asha"))
                .andExpect(jsonPath("$.status").value("OPEN"));
    }

    @Test
    void blankTitle_returns400() throws Exception {
        send(post("/api/tickets"), "asha", "{\"title\": \"   \"}").andExpect(status().isBadRequest());
    }

    // ---------- view ticket ----------

    @Test
    void owner_canViewTheirTicket() throws Exception {
        createTicket("asha", "Order not delivered");
        send(get("/api/tickets/1"), "asha", null)
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Order not delivered"));
    }

    @Test
    void anotherCustomer_gets403() throws Exception {
        createTicket("asha", "Order not delivered");
        send(get("/api/tickets/1"), "ravi", null).andExpect(status().isForbidden());
    }

    @Test
    void agent_canViewAnyTicket() throws Exception {
        createTicket("asha", "Order not delivered");
        send(get("/api/tickets/1"), "neha", null).andExpect(status().isOk());
    }

    @Test
    void unknownTicket_returns404() throws Exception {
        send(get("/api/tickets/99"), "asha", null).andExpect(status().isNotFound());
    }

    // ---------- replies ----------

    @Test
    void reply_isSavedAndShownOnTheTicket() throws Exception {
        createTicket("asha", "Order not delivered");
        send(post("/api/tickets/1/replies"), "neha", "{\"message\": \"Checking with courier\"}")
                .andExpect(status().isCreated());

        send(get("/api/tickets/1"), "asha", null)
                .andExpect(jsonPath("$.replies", hasSize(1)))
                .andExpect(jsonPath("$.replies[0].author").value("neha"))
                .andExpect(jsonPath("$.replies[0].message").value("Checking with courier"));
    }

    @Test
    void blankReply_returns400() throws Exception {
        createTicket("asha", "Order not delivered");
        send(post("/api/tickets/1/replies"), "neha", "{\"message\": \"\"}").andExpect(status().isBadRequest());
    }

    // ---------- change status ----------

    @Test
    void agent_canMoveTicketToInProgress() throws Exception {
        createTicket("asha", "Order not delivered");
        send(patch("/api/tickets/1/status"), "neha", "{\"status\": \"IN_PROGRESS\"}")
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
    }

    @Test
    void customer_cannotChangeStatus() throws Exception {
        createTicket("asha", "Order not delivered");
        send(patch("/api/tickets/1/status"), "asha", "{\"status\": \"CLOSED\"}").andExpect(status().isForbidden());
    }

    @Test
    void closedTicket_cannotChangeStatus() throws Exception {
        createTicket("asha", "Order not delivered");
        send(patch("/api/tickets/1/status"), "neha", "{\"status\": \"CLOSED\"}");
        send(patch("/api/tickets/1/status"), "neha", "{\"status\": \"OPEN\"}").andExpect(status().isConflict());
    }

    // ---------- list tickets ----------

    @Test
    void customer_seesOnlyTheirOwnTickets() throws Exception {
        createTicket("asha", "A1");
        createTicket("ravi", "R1");
        send(get("/api/tickets"), "ravi", null).andExpect(jsonPath("$[*].title", contains("R1")));
    }

    @Test
    void fivePerPage_newestFirst() throws Exception {
        for (int i = 1; i <= 6; i++) {
            createTicket("asha", "T" + i);
        }
        send(get("/api/tickets").param("page", "1"), "asha", null)
                .andExpect(jsonPath("$[*].title", contains("T6", "T5", "T4", "T3", "T2")));
        send(get("/api/tickets").param("page", "2"), "asha", null)
                .andExpect(jsonPath("$[*].title", contains("T1")));
    }

    // ---------- notifications ----------

    @Test
    void count_includesOnlyRepliesFromOthers() throws Exception {
        repository.save(new Ticket(null, "Late order", "", "asha", "OPEN",
                List.of(new Reply("asha", "Any update?"), new Reply("neha", "Arriving today"))));
        send(get("/api/notifications/count"), "asha", null).andExpect(jsonPath("$.count").value(1));
    }
}
