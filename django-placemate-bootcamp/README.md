# PlaceMate (Django) – Debugging Bootcamp

PlaceMate is a **campus placement portal**: students see drives, save them, check eligibility and apply; the placement office (TPO) closes drives and builds the shortlist.

The project has **6 missions**. Each mission is one part of the app that is broken, with its own test file. The bugs get closer to the real Amazon repository round as you go: Mission 6 is a full Amazon-style task.

| Mission | Topic | Endpoint(s) | Test file | Bugs | Time |
|---|---|---|---|---|---|
| 1 | Python essentials | `GET /api/students/me/summary` | `tests/test_m1_python.py` | 5 | 20 min |
| 2 | Request lifecycle (URL → view → response) | `/api/drives/…` list, detail, save, notes | `tests/test_m2_request_lifecycle.py` | 5 | 20 min |
| 3 | Views and services (status codes, errors, JSON shape) | `POST /api/drives/<id>/apply`, `GET /api/applications/me` | `tests/test_m3_views_services.py` | 4 | 20 min |
| 4 | Django ORM | search, stats, withdraw, application detail, my applications | `tests/test_m4_orm.py` | 5 | 25 min |
| 5 | Authentication and business rules | eligibility, close drive | `tests/test_m5_auth_business.py` | 5 | 20 min |
| 6 | **Practical challenge (Amazon level)** | `GET /api/drives/<id>/shortlist` (+ confirm) | `tests/test_m6_shortlist.py` | 6 | 60 min |

Missions are independent: a bug in one mission never breaks another mission's tests.

## Setup (once)

```bash
git clone https://github.com/govindchandak/Amazon-debugging-question.git
cd Amazon-debugging-question/django-placemate-bootcamp
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # Mac / Linux
pip install -r requirements.txt
```

Run one mission's tests (always from this folder):

```bash
pytest tests/test_m1_python.py            # one mission
pytest tests/test_m1_python.py -x -vv     # stop at the first failure, show full detail
pytest -k "tags"                           # only tests whose name contains "tags"
pytest                                     # everything (31 tests)
```

Try the API by hand:

```bash
python manage.py migrate
python manage.py seed_db       # resets the data
python manage.py runserver
```

Demo logins (`POST /api/auth/login` with `{"email": ..., "password": "Password@123"}` returns a token; send it as `Authorization: Bearer <token>`): student `sam.rivera@email.com`, student `priya.nair@email.com`, placement office `tpo@college.edu`.

## Rules (same as the Amazon round)

1. Make all the tests of the mission pass. **Do not edit the tests.**
2. Use the failing tests to find the bug: test name → assertion → expected vs actual → the code path.
3. Make the smallest fix. Re-run **all** tests of the mission after every fix.
4. Start a mission over: `git checkout -- .`

## Project map

```
placemate/        settings.py (apps, middleware), urls.py (top-level routes)
accounts/         Student + AuthToken models, middleware.py (Bearer token, login_required_api, tpo_required),
                  summary.py (Mission 1), views.py
drives/           Company, Drive, SavedDrive, DriveNote models, urls.py, views.py (Missions 2, 4, 5),
                  rules.py (eligibility rules, Mission 5), serializers.py, management/commands/seed_db.py
applications/     Application model, services.py + views.py (Missions 3, 4, 6), serializers.py
tests/            conftest.py (helpers) and one test file per mission
```

---

## Mission 1 – Python essentials

**Issue:** the profile card on the student dashboard shows wrong numbers. The average test score loses its decimals, one student sees another student's skill tags, dream packages are in a strange order, `dreamReady` is not `true`/`false`, and top skills with the same level are in the wrong order.

`GET /api/students/me/summary` (login required) → `200`

```json
{
  "summary": {
    "name": "Sam Rivera", "rollNo": "21CS001", "cgpa": 8.4,
    "averageTestScore": 76.5,
    "topSkills": ["Python", "Django", "SQL"],
    "tags": ["#python", "#sql", "#django"],
    "targetCtcs": [45.0, 12.5, 9.0],
    "band": "A",
    "dreamReady": true
  }
}
```

| Field | Rule |
|---|---|
| averageTestScore | mean of `test_scores`, rounded to 1 decimal; `null` if there are none |
| topSkills | at most 3 names, highest `level` first; equal levels A→Z |
| tags | `#` + lower-case name (spaces → `-`); a skill appears once even if repeated in another case; **only this student's skills** |
| targetCtcs | the student's dream packages as **numbers**, highest first |
| band | CGPA ≥ 8.0 → A, ≥ 7.0 → B, ≥ 6.0 → C, else D |
| dreamReady | `true` for band A or B, otherwise `false` (a real boolean) |

## Mission 2 – Request lifecycle

**Issue:** several drive pages fail before any business logic runs: crashes, 404s and 405s.

| Request | Expected |
|---|---|
| `GET /api/drives/` | `200` with a **JSON array** of OPEN drives, earliest deadline first |
| `GET /api/drives/<id>` | `200 {"drive": {...}}`, `404` if not found |
| `POST /api/drives/<id>/save` (login) | `201 {"message": "Drive saved"}` (`200` "Drive already saved") |
| `DELETE /api/drives/<id>/save` (login) | `200 {"message": "Drive removed from saved list"}` |
| `POST /api/drives/<id>/notes` (login), JSON body `{"note": "..."}` | `201 {"message": "Note added", "note": {"_id", "text"}}`, `400` if the note is empty |

## Mission 3 – Views and services

**Issue:** applying to a drive crashes, and the API does not follow the error contract.

`POST /api/drives/<id>/apply` (login)

| Case | Status | Body |
|---|---|---|
| Success | **201** | `{"message": "Application submitted", "application": {...}}` |
| Already applied (active application) | **409** | `{"error": "ALREADY_APPLIED", "message": ...}` |
| Drive closed or deadline passed | 409 | `{"error": "DRIVE_CLOSED", ...}` |
| Profile does not meet the criteria | **422** | `{"error": "NOT_ELIGIBLE", "message": "<first reason>"}` |

Application JSON (used everywhere): `{"_id", "driveId", "company", "role", "status", "appliedAt"}`. `GET /api/applications/me` returns `{"applications": [...]}`.

## Mission 4 – Django ORM

**Issue:** search, stats and withdrawals give wrong data.

| Request | Expected |
|---|---|
| `GET /api/drives/search?minCtc=8.4&skill=python` | OPEN drives with company CTC **≥** minCtc; `skill` matches a required skill, any case |
| `GET /api/drives/stats` | per drive, `activeApplications` = applications with status `APPLIED` only |
| `POST /api/applications/<id>/withdraw` | status becomes `WITHDRAWN` **in the database**; `409` if not active |
| `GET /api/applications/<id>` | own application only; anything else (missing or another student's) → **404**, never 500 |
| `GET /api/applications/me` | **newest first** |

## Mission 5 – Authentication and business rules

**Issue:** anyone can close drives, and eligible students are told they are not eligible.

- `GET /api/drives/<id>/eligibility` needs login (`401` without a token) → `{"driveId", "eligible", "reasons": [...]}`.
- `POST /api/drives/<id>/close` is for the placement office only: student → **403**, TPO → `200`.
- Eligibility rules (`drives/rules.py`): branch is one of the drive's branches (**case does not matter**), `cgpa >= minCgpa`, `backlogs <= maxBacklogs`; plus the drive must be OPEN and before its deadline.

| Code | Meaning |
|---|---|
| 401 | not logged in (no or invalid token) |
| 403 | logged in, but not allowed |
| 404 | the thing does not exist (or is not yours) |
| 409 | conflicts with the current state (already applied, already closed) |
| 422 | valid request, but a business rule says no |

## Mission 6 – Practical challenge: drive shortlist (Amazon level, 60 minutes)

**Issue:** the placement office builds the shortlist for a drive, but the page shows nothing useful. Once that is fixed, the wrong students are shortlisted and confirming the shortlist does not stick.

**Steps to reproduce:** log in as `tpo@college.edu`, open `GET /api/drives/1/shortlist`, then `POST /api/drives/1/shortlist/confirm`.

`GET /api/drives/<id>/shortlist` (TPO only) → `200`

```json
{
  "message": "Shortlisted 2 of 2 eligible applicants",
  "shortlist": [
    {"rank": 1, "applicationId": "7", "studentId": "2", "name": "Ben", "rollNo": "21CS002", "score": 0.84, "matchedSkills": ["Python", "SQL"]}
  ]
}
```

No eligible applicants: `{"message": "No eligible applicants yet", "shortlist": []}`

**Who can be ranked**

| Rule | Details |
|---|---|
| Status | only `APPLIED` applications (withdrawn ones never count) |
| Profile | the student must still meet the drive criteria (Mission 5 rules) |
| Test score | applications without a `test_score` are not ranked yet |

**Score formula**

```
score = (cgpa / 10) × 0.4 + (testScore / 100) × 0.4 + skillMatch × 0.2
```

| Variable | Definition |
|---|---|
| skillMatch | required skills of the drive the student has (**any case**) / number of required skills; 1.0 if the drive lists none |
| matchedSkills | the matched skills, written as in the drive, in the drive's order |

**Ordering and limits:** score high → low; equal scores → **higher CGPA first**, then roll number A→Z. Take only the first `seats` students. `score` is rounded to 3 decimals in the response. The message is `Shortlisted <taken> of <ranked> eligible applicants`.

`POST /api/drives/<id>/shortlist/confirm` (TPO) sets the status of exactly the shortlisted applications to `SHORTLISTED` **and saves it**; returns `{"message", "count"}`.

**Worked example:** drive requires `Python`, `SQL`. Ben: CGPA 9.0, test 70, has Python and SQL → 0.36 + 0.28 + 0.2 = **0.84**. Asha: CGPA 8.0, test 90, has only Python → 0.32 + 0.36 + 0.1 = **0.78**. Ben ranks first.
