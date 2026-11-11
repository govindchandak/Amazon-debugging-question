package com.practice.returns;

import com.practice.returns.repository.OrderRepository;
import com.practice.returns.repository.ReturnRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

import java.time.LocalDate;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class ReturnControllerTest {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private OrderRepository orders;

    @Autowired
    private ReturnRepository returns;

    @BeforeEach
    void cleanDatabase() {
        orders.deleteAll();
        returns.deleteAll();
    }

    /** Creates an order through the API. Orders get ids 1, 2, 3 ... in order. */
    private void createOrder(String customerId, long priceInPaise, String status, Integer deliveredDaysAgo) throws Exception {
        String deliveredOn = deliveredDaysAgo == null ? "null" : "\"" + LocalDate.now().minusDays(deliveredDaysAgo) + "\"";
        String body = "{\"customerId\": \"" + customerId + "\", \"priceInPaise\": " + priceInPaise
                + ", \"status\": \"" + status + "\", \"deliveredOn\": " + deliveredOn + "}";
        mvc.perform(post("/api/orders").contentType(MediaType.APPLICATION_JSON).content(body))
                .andExpect(status().isCreated());
    }

    private ResultActions requestReturn(long orderId, String reason) throws Exception {
        String body = "{\"orderId\": " + orderId + ", \"reason\": \"" + reason + "\"}";
        return mvc.perform(post("/api/returns").contentType(MediaType.APPLICATION_JSON).content(body));
    }

    // ---------- refund amount ----------

    @Test
    void return_chargesTenPercentRestockingFee() throws Exception {
        createOrder("asha", 100000, "DELIVERED", 5);
        requestReturn(1, "CHANGED_MIND")
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.refundInPaise").value(90000));
    }

    @Test
    void return_ofDamagedItem_getsFullRefund() throws Exception {
        createOrder("asha", 100000, "DELIVERED", 5);
        requestReturn(1, "DAMAGED")
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.refundInPaise").value(100000));
    }

    // ---------- who can return ----------

    @Test
    void return_ofUnknownOrder_returns404() throws Exception {
        requestReturn(42, "CHANGED_MIND").andExpect(status().isNotFound());
    }

    @Test
    void return_ofShippedOrder_returns400() throws Exception {
        createOrder("asha", 50000, "SHIPPED", null);
        requestReturn(1, "CHANGED_MIND").andExpect(status().isBadRequest());
    }

    @Test
    void return_onDay30_isAllowed() throws Exception {
        createOrder("asha", 50000, "DELIVERED", 30);
        requestReturn(1, "CHANGED_MIND").andExpect(status().isCreated());
    }

    @Test
    void return_onDay31_returns400() throws Exception {
        createOrder("asha", 50000, "DELIVERED", 31);
        requestReturn(1, "CHANGED_MIND").andExpect(status().isBadRequest());
    }

    // ---------- one return per order ----------

    @Test
    void return_ofSameOrderTwice_returns409() throws Exception {
        createOrder("asha", 50000, "DELIVERED", 3);
        requestReturn(1, "CHANGED_MIND").andExpect(status().isCreated());
        requestReturn(1, "CHANGED_MIND").andExpect(status().isConflict());
    }

    @Test
    void customer_canReturnTwoDifferentOrders() throws Exception {
        createOrder("asha", 50000, "DELIVERED", 3);
        createOrder("asha", 70000, "DELIVERED", 3);
        requestReturn(1, "CHANGED_MIND").andExpect(status().isCreated());
        requestReturn(2, "CHANGED_MIND").andExpect(status().isCreated());
    }

    // ---------- listing ----------

    @Test
    void list_showsOnlyThisCustomersReturns() throws Exception {
        createOrder("asha", 50000, "DELIVERED", 3);
        createOrder("ravi", 70000, "DELIVERED", 3);
        requestReturn(1, "CHANGED_MIND");
        requestReturn(2, "CHANGED_MIND");

        mvc.perform(get("/api/returns").param("customerId", "asha"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].orderId").value(1));
    }
}
