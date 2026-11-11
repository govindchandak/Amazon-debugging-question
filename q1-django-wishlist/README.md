# Q1 · Wishlist · Django · Easy

**3 bugs · 30 minutes · 7 tests (3 failing at the start)**

Customers save products they like to a wishlist and see them on a wishlist page.

## What customers are reporting

1. "I click *Add to wishlist* and get a success message, but my wishlist stays empty."
2. "Bob can't save a Kindle. He gets *Already in wishlist*, but only Alice saved one."
3. "The wishlist page always says *Your wishlist is empty*, even when the API shows items."

## How it should work

| Rule | Expected |
|---|---|
| Save a product | `201`, and the item shows up in the wishlist |
| Same customer saves the same product again | `409 Conflict` |
| Two different customers save the same product | Both get `201` |
| Product id does not exist | `404 Not Found` |
| Wishlist page `/wishlist/<customer>/` | Lists every saved item and the total price |

## API

| Method | URL | Body |
|---|---|---|
| GET | `/api/products/` | |
| POST | `/api/wishlist/<customer>/items/` | `{"product_id": 1}` |
| GET | `/api/wishlist/<customer>/` | |
| GET | `/wishlist/<customer>/` (HTML page) | |

## Where things are

```
wishlist/
├── models.py          Product, WishlistItem (the database tables)
├── urls.py            URL → view
├── views.py           the logic for each URL
├── templates/wishlist/page.html
└── tests.py           the tests you must make pass (do not edit)
```

## Run

```bash
cd q1-django-wishlist
pip install -r requirements.txt
python manage.py test                 # run the tests
```

Try it in the browser (optional):

```bash
python manage.py migrate
python manage.py seed                 # adds 3 sample products
python manage.py runserver            # open http://127.0.0.1:8000/wishlist/alice/
```

**Done when:** `python manage.py test` prints `OK`.
