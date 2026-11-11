# Q5 · Gift Card Wallet · Node.js (Express) · Easy

**3 bugs · 30 minutes · 7 tests (5 failing at the start)**

Customers keep Amazon gift cards in a wallet and spend from them.

## What customers are reporting

1. "Adding a card or spending from it always fails with *Internal server error*."
2. "After that was fixed: every new card says *This card is already in your wallet*, even brand-new codes."
3. "Opening a card by its id says *Card not found*, but the card is in my list."

Report 2 only shows up after report 1 is fixed. That happens in the real round too.

## How it should work

| Rule | Expected |
|---|---|
| Add a card `{code, balance}` | `201` with the new card |
| Same code added again | `409` |
| Get a card by id | `200`, or `404` if the id does not exist |
| Spend `{amount}` | `200` with the new balance |
| Spend more than the balance | `400` |

## API

| Method | URL | Body |
|---|---|---|
| GET | `/api/cards` | |
| POST | `/api/cards` | `{"code": "AMZ-222", "balance": 1000}` |
| GET | `/api/cards/:id` | |
| POST | `/api/cards/:id/spend` | `{"amount": 120}` |

## Where things are

```
src/
├── app.js                       creates the app, adds middleware and routes
├── routes/cardRoutes.js         URL → controller function
├── controllers/cardController.js
├── data/store.js                the "database" (async, like Mongoose)
├── middleware/errorHandler.js
└── utils/httpError.js
tests/cards.test.js              do not edit
```

## Run

```bash
cd q5-node-gift-wallet
npm install          # once
npm test             # run the tests
npm start            # http://localhost:3000/api/cards
```

**Done when:** `npm test` shows `Tests: 7 passed, 7 total`.
