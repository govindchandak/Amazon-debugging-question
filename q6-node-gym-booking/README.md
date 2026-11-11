# Q6 · Gym Class Booking · Node.js (Express) · Medium

**5 bugs · 50 minutes · 12 tests (5 failing at the start)**

Gym members book seats in classes. When a class is full they join a waitlist. A trainer can see who booked.

No complaints this time. Read the rules, run the tests and find what is wrong.

## How it should work

| Rule | Expected |
|---|---|
| Who is calling | `X-Member` header: `asha`, `ravi`, `kiran` (members) or `neha` (trainer). Missing or unknown → `401` |
| Book a class with free seats | `201`, status `BOOKED` |
| Book when every seat is taken (booked = capacity) | `201`, status `WAITLISTED` |
| Already booked **or** already on the waitlist | `409` |
| Cancel a booking | The seat goes to the **first** member who joined the waitlist |
| Cancel with no booking | `404` |
| Attendee list `/attendees` | Trainers only. Members get `403` |
| Rate limit | At most 5 booking requests (book or cancel) per **member** per minute. The 6th gets `429` |

## API

| Method | URL |
|---|---|
| GET | `/api/classes/:id` |
| POST | `/api/classes/:id/book` |
| DELETE | `/api/classes/:id/book` |
| GET | `/api/classes/:id/attendees` |

## Where things are

```
src/
├── app.js
├── routes/classRoutes.js
├── middleware/auth.js           who is calling
├── middleware/rateLimit.js      5 booking requests per minute
├── controllers/classController.js
├── services/bookingService.js   booking rules
└── data/store.js                the "database"
tests/booking.test.js            do not edit
```

## Run

```bash
cd q6-node-gym-booking
npm install
npm test
```

**Done when:** `npm test` shows `Tests: 12 passed, 12 total`.
