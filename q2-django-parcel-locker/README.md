# Q2 · Parcel Locker · Django · Medium

**4 bugs · 45 minutes · 11 tests (5 failing at the start)**

A pickup point has lockers in three sizes. A delivery agent puts a parcel in a locker, and the customer gets a 6-digit code to collect it.

No customer complaints this time. Read the rules, run the tests and work out what is wrong.

## How it should work

| Rule | Expected |
|---|---|
| Sizes | `S` < `M` < `L`. A parcel fits in a locker of its size **or bigger**. |
| Deposit | Uses the **smallest** free locker that fits. Returns `201`, locker code and a 6-digit pickup code. |
| No free locker that fits | `409` |
| Same tracking id deposited twice | `409` |
| Pickup with the right code | `200`, status `PICKED_UP`, and the locker is **free again** |
| Pickup with a wrong code | `403` |
| Pickup window | Up to 3 full days. From 3 days (72 hours) after deposit, pickup returns `410 Gone`. |
| Free lockers for a size | Counts free lockers of that size **or bigger** |

## API

| Method | URL | Body |
|---|---|---|
| POST | `/api/parcels/deposit/` | `{"tracking_id": "AMZ1", "size": "M"}` |
| POST | `/api/parcels/pickup/` | `{"tracking_id": "AMZ1", "code": "042917"}` |
| GET | `/api/lockers/free/?size=M` | |

## Where things are

```
lockers/
├── models.py      Locker, Parcel
├── services.py    business rules (deposit, pickup, counting)
├── views.py       reads the request, calls services, returns JSON
├── urls.py
└── tests.py       do not edit
```

## Run

```bash
cd q2-django-parcel-locker
pip install -r requirements.txt
python manage.py test
```

**Tip:** one test shows `ERROR` instead of `FAIL`. That means the code crashed. Read the last lines of the traceback first.

**Done when:** `python manage.py test` prints `OK`.
