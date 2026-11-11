# Worked example · HelpDesk (Django, Spring Boot and Node.js)

The same support-ticket app built in all three Amazon stacks, with the **same 9 bugs** and the **same 16 tests** (10 failing at the start).

The study guide walks through every bug, step by step, in your stack. Try it yourself first, then follow along.

| Folder | Stack | Run the tests |
|---|---|---|
| [`django/`](django) | Python + Django | `python manage.py test` |
| [`springboot/`](springboot) | Java + Spring Boot | `mvn test` |
| [`express/`](express) | Node.js + Express | `npm install` then `npm test` |

## The app

Customers raise support tickets. Agents reply and move tickets through `OPEN → IN_PROGRESS → RESOLVED → CLOSED`.

Who is calling comes from the `X-User` header: `asha` and `ravi` are customers, `neha` is an agent.

## How it should work

| Rule | Expected |
|---|---|
| No `X-User` header, or an unknown user | `401` |
| Create a ticket | `201`, status `OPEN` |
| Blank or missing title | `400` |
| View a ticket | Owner or any agent: `200`. Another customer: `403`. Unknown id: `404` |
| Reply `POST /api/tickets/{id}/replies` | `201`, and the reply shows on the ticket. Blank message: `400` |
| Change status (agents only) | `200`. Customer: `403`. A `CLOSED` ticket cannot change: `409` |
| List tickets `?page=1` | Customers see only their own, agents see all. Newest first, 5 per page |
| `GET /api/notifications/count` | Replies on my tickets written by **someone else** |

## API

| Method | URL | Body |
|---|---|---|
| POST | `/api/tickets` | `{"title": "Refund missing", "description": "..."}` |
| GET | `/api/tickets?page=1` | |
| GET | `/api/tickets/{id}` | |
| POST | `/api/tickets/{id}/replies` | `{"message": "Checking with courier"}` |
| PATCH | `/api/tickets/{id}/status` | `{"status": "IN_PROGRESS"}` |
| GET | `/api/notifications/count` | |
