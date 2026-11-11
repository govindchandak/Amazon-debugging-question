const request = require('supertest');
const app = require('../src/app');
const { Classes } = require('../src/data/store');
const { resetLimits } = require('../src/middleware/rateLimit');

const as = (member) => ({ 'X-Member': member });
const book = (member, id = 1) => request(app).post(`/api/classes/${id}/book`).set(as(member));
const cancel = (member, id = 1) => request(app).delete(`/api/classes/${id}/book`).set(as(member));
const attendees = (member, id = 1) => request(app).get(`/api/classes/${id}/attendees`).set(as(member));

beforeEach(async () => {
  await Classes.deleteAll();
  resetLimits();
});

describe('booking', () => {
  test('booking a class with free seats returns BOOKED', async () => {
    await Classes.create({ name: 'Yoga', capacity: 2 });
    const res = await book('asha');
    expect(res.status).toBe(201);
    expect(res.body.status).toBe('BOOKED');
  });

  test('when the class is full, the next member is WAITLISTED', async () => {
    await Classes.create({ name: 'Yoga', capacity: 2 });
    await book('asha');
    await book('ravi');
    const res = await book('kiran');
    expect(res.body.status).toBe('WAITLISTED');
  });

  test('booking the same class twice returns 409', async () => {
    await Classes.create({ name: 'Yoga', capacity: 2 });
    await book('asha');
    const res = await book('asha');
    expect(res.status).toBe(409);
  });

  test('a waitlisted member booking again returns 409', async () => {
    await Classes.create({ name: 'Spin', capacity: 1, booked: ['asha'], waitlist: ['ravi'] });
    const res = await book('ravi');
    expect(res.status).toBe(409);
  });

  test('unknown class returns 404', async () => {
    const res = await book('asha', 99);
    expect(res.status).toBe(404);
  });

  test('request without X-Member returns 401', async () => {
    await Classes.create({ name: 'Yoga', capacity: 2 });
    const res = await request(app).post('/api/classes/1/book');
    expect(res.status).toBe(401);
  });
});

describe('cancelling', () => {
  test('cancelling gives the seat to the FIRST member on the waitlist', async () => {
    await Classes.create({ name: 'Spin', capacity: 1, booked: ['asha'], waitlist: ['ravi', 'kiran'] });
    await cancel('asha');
    const res = await attendees('neha');
    expect(res.body).toEqual({ booked: ['ravi'], waitlist: ['kiran'] });
  });

  test('cancelling without a booking returns 404', async () => {
    await Classes.create({ name: 'Yoga', capacity: 2 });
    const res = await cancel('asha');
    expect(res.status).toBe(404);
  });
});

describe('attendee list', () => {
  test('trainer can see attendees', async () => {
    await Classes.create({ name: 'Yoga', capacity: 2, booked: ['asha'] });
    const res = await attendees('neha');
    expect(res.status).toBe(200);
    expect(res.body.booked).toEqual(['asha']);
  });

  test('member gets 403', async () => {
    await Classes.create({ name: 'Yoga', capacity: 2, booked: ['asha'] });
    const res = await attendees('ravi');
    expect(res.status).toBe(403);
  });
});

describe('rate limit', () => {
  test('the 6th booking request in a minute returns 429', async () => {
    await Classes.create({ name: 'Yoga', capacity: 10 });
    for (let i = 0; i < 5; i++) await book('asha');
    const res = await book('asha');
    expect(res.status).toBe(429);
  });

  test('the limit is per member: one busy member does not block another', async () => {
    await Classes.create({ name: 'Yoga', capacity: 10 });
    for (let i = 0; i < 5; i++) await book('asha');
    const res = await book('ravi');
    expect(res.status).toBe(201);
  });
});
