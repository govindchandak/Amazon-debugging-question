# Q3 · Task Board · Spring Boot · Easy

**3 bugs · 30 minutes · 6 tests (3 failing at the start)**

A team keeps its tasks on a board. Each task has a title, a priority (1 = high, 3 = low) and a status.

## What users are reporting

1. "I move a task to DONE and the response says DONE, but when I reload the board it is back to TODO."
2. "Updating a task that doesn't exist gives a 500 Internal Server Error. It should say 404."
3. "Urgent tasks show up at the bottom of the board."

## How it should work

| Rule | Expected |
|---|---|
| Create a task | `201`, status `TODO` |
| Blank title, or priority not 1-3 | `400` |
| Change status | `200`, and the change is **saved** |
| Task id does not exist | `404` |
| List tasks | Priority 1 first, then 2, then 3. Same priority: older task first. |
| `?status=DONE` | Only tasks with that status |

## API

| Method | URL | Body |
|---|---|---|
| POST | `/api/tasks` | `{"title": "Fix login", "priority": 1}` |
| PATCH | `/api/tasks/{id}/status` | `{"status": "DONE"}` |
| GET | `/api/tasks` or `/api/tasks?status=TODO` | |

## Where things are

```
src/main/java/com/practice/taskboard/
├── controller/TaskController.java   URL → method
├── service/TaskService.java         business rules
├── repository/TaskRepository.java   the "database" (in memory)
├── model/Task.java, TaskStatus.java
└── dto/                             request bodies
src/test/java/.../TaskControllerTest.java   do not edit
```

> The repository works like a real database: it gives you a **copy** of the data. A change is kept only after you call `save()`.

## Run

```bash
cd q3-spring-task-board
mvn test                  # run the tests
mvn spring-boot:run       # start the app on http://localhost:8080
```

In IntelliJ: open this folder, wait for Maven to load, right-click `TaskControllerTest` → **Run**.

**Done when:** `mvn test` shows `Tests run: 6, Failures: 0, Errors: 0` and `BUILD SUCCESS`.
