# Q4 · Returns Desk · Spring Boot · Medium

**4 bugs · 45 minutes · 9 tests (4 failing at the start)**

Customers ask to return an order. The service checks whether the return is allowed and works out the refund.

No customer complaints this time. Read the rules, run the tests and work out what is wrong.

## How it should work

| Rule | Expected |
|---|---|
| Order id does not exist | `404` |
| Only `DELIVERED` orders can be returned (not `SHIPPED`, not `CANCELLED`) | else `400` |
| Return window: up to 30 days after delivery. **Day 30 is allowed**, day 31 is not. | else `400` |
| One return per **order**. A customer can return two different orders. | same order again → `409` |
| Refund: price minus a 10% restocking fee | ₹1,000 order → ₹900 refund |
| Reason `DAMAGED` | Full refund, no fee |
| List returns | Only that customer's returns |

Money is stored in **paise** (₹1 = 100 paise), so ₹1,000 is `100000`.

## API

| Method | URL | Body |
|---|---|---|
| POST | `/api/orders` | `{"customerId": "asha", "priceInPaise": 100000, "status": "DELIVERED", "deliveredOn": "2026-11-01"}` |
| POST | `/api/returns` | `{"orderId": 1, "reason": "DAMAGED"}` |
| GET | `/api/returns?customerId=asha` | |

## Where things are

```
src/main/java/com/practice/returns/
├── controller/   OrderController, ReturnController
├── service/      ReturnService (business rules)
├── repository/   OrderRepository, ReturnRepository (in memory)
├── model/        Order, ReturnRequest
└── dto/          request bodies
src/test/java/.../ReturnControllerTest.java   do not edit
```

## Run

```bash
cd q4-spring-returns-desk
mvn test
mvn spring-boot:run
```

**Tip:** one test fails with an exception instead of a wrong status. Scroll to the first `Caused by:` line.

**Done when:** `mvn test` shows `Tests run: 9, Failures: 0, Errors: 0` and `BUILD SUCCESS`.
