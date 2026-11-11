const request = require('supertest');
const app = require('../src/app');
const { Cards } = require('../src/data/store');

beforeEach(async () => {
  await Cards.deleteAll();
});

test('list cards', async () => {
  await Cards.create({ code: 'AMZ-111', balance: 500 });
  const res = await request(app).get('/api/cards');
  expect(res.status).toBe(200);
  expect(res.body).toHaveLength(1);
});

test('add a new card returns 201', async () => {
  const res = await request(app).post('/api/cards').send({ code: 'AMZ-222', balance: 1000 });
  expect(res.status).toBe(201);
  expect(res.body).toMatchObject({ id: 1, code: 'AMZ-222', balance: 1000 });
});

test('adding the same code twice returns 409', async () => {
  await Cards.create({ code: 'AMZ-111', balance: 500 });
  const res = await request(app).post('/api/cards').send({ code: 'AMZ-111', balance: 500 });
  expect(res.status).toBe(409);
});

test('get one card by id', async () => {
  await Cards.create({ code: 'AMZ-111', balance: 500 });
  const res = await request(app).get('/api/cards/1');
  expect(res.status).toBe(200);
  expect(res.body.code).toBe('AMZ-111');
});

test('unknown card returns 404', async () => {
  const res = await request(app).get('/api/cards/42');
  expect(res.status).toBe(404);
});

test('spend reduces the balance', async () => {
  await Cards.create({ code: 'AMZ-111', balance: 500 });
  const res = await request(app).post('/api/cards/1/spend').send({ amount: 120 });
  expect(res.status).toBe(200);
  expect(res.body.balance).toBe(380);
});

test('spending more than the balance returns 400', async () => {
  await Cards.create({ code: 'AMZ-111', balance: 500 });
  const res = await request(app).post('/api/cards/1/spend').send({ amount: 501 });
  expect(res.status).toBe(400);
});
