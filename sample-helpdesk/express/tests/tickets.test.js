const request = require('supertest');
const app = require('../src/app');
const { Tickets } = require('../src/data/store');

const as = (user) => ({ 'X-User': user });

async function createTicket(user, title = 'Order not delivered') {
  const res = await request(app).post('/api/tickets').set(as(user)).send({ title, description: 'Details' });
  return res.body;
}

beforeEach(async () => {
  await Tickets.deleteAll();
});

describe('who is calling', () => {
  test('request without X-User header returns 401', async () => {
    const res = await request(app).get('/api/tickets');
    expect(res.status).toBe(401);
  });

  test('unknown user returns 401', async () => {
    const res = await request(app).get('/api/tickets').set(as('hacker'));
    expect(res.status).toBe(401);
  });
});

describe('create ticket', () => {
  test('returns 201 with status OPEN', async () => {
    const res = await request(app).post('/api/tickets').set(as('asha')).send({ title: 'Refund missing' });
    expect(res.status).toBe(201);
    expect(res.body).toMatchObject({ id: 1, title: 'Refund missing', owner: 'asha', status: 'OPEN' });
  });

  test('blank title returns 400', async () => {
    const res = await request(app).post('/api/tickets').set(as('asha')).send({ title: '   ' });
    expect(res.status).toBe(400);
  });
});

describe('view ticket', () => {
  test('owner can view their ticket', async () => {
    await createTicket('asha');
    const res = await request(app).get('/api/tickets/1').set(as('asha'));
    expect(res.status).toBe(200);
    expect(res.body.title).toBe('Order not delivered');
  });

  test('another customer gets 403', async () => {
    await createTicket('asha');
    const res = await request(app).get('/api/tickets/1').set(as('ravi'));
    expect(res.status).toBe(403);
  });

  test('agent can view any ticket', async () => {
    await createTicket('asha');
    const res = await request(app).get('/api/tickets/1').set(as('neha'));
    expect(res.status).toBe(200);
  });

  test('unknown ticket returns 404', async () => {
    const res = await request(app).get('/api/tickets/99').set(as('asha'));
    expect(res.status).toBe(404);
  });
});

describe('replies', () => {
  test('reply is saved and shown on the ticket', async () => {
    await createTicket('asha');
    const res = await request(app).post('/api/tickets/1/replies').set(as('neha')).send({ message: 'Checking with courier' });
    expect(res.status).toBe(201);

    const ticket = await request(app).get('/api/tickets/1').set(as('asha'));
    expect(ticket.body.replies).toEqual([{ author: 'neha', message: 'Checking with courier' }]);
  });

  test('blank reply returns 400', async () => {
    await createTicket('asha');
    const res = await request(app).post('/api/tickets/1/replies').set(as('neha')).send({ message: '' });
    expect(res.status).toBe(400);
  });
});

describe('change status', () => {
  test('agent can move a ticket to IN_PROGRESS', async () => {
    await createTicket('asha');
    const res = await request(app).patch('/api/tickets/1/status').set(as('neha')).send({ status: 'IN_PROGRESS' });
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('IN_PROGRESS');
  });

  test('customer cannot change status (403)', async () => {
    await createTicket('asha');
    const res = await request(app).patch('/api/tickets/1/status').set(as('asha')).send({ status: 'CLOSED' });
    expect(res.status).toBe(403);
  });

  test('closed ticket cannot change status (409)', async () => {
    await createTicket('asha');
    await request(app).patch('/api/tickets/1/status').set(as('neha')).send({ status: 'CLOSED' });
    const res = await request(app).patch('/api/tickets/1/status').set(as('neha')).send({ status: 'OPEN' });
    expect(res.status).toBe(409);
  });
});

describe('list tickets', () => {
  test('customer sees only their own tickets', async () => {
    await createTicket('asha', 'A1');
    await createTicket('ravi', 'R1');
    const res = await request(app).get('/api/tickets').set(as('ravi'));
    expect(res.body.map((t) => t.title)).toEqual(['R1']);
  });

  test('5 per page, newest first', async () => {
    for (let i = 1; i <= 6; i++) await createTicket('asha', `T${i}`);
    const page1 = await request(app).get('/api/tickets?page=1').set(as('asha'));
    const page2 = await request(app).get('/api/tickets?page=2').set(as('asha'));
    expect(page1.body.map((t) => t.title)).toEqual(['T6', 'T5', 'T4', 'T3', 'T2']);
    expect(page2.body.map((t) => t.title)).toEqual(['T1']);
  });
});

describe('notifications', () => {
  test('counts only replies written by someone else', async () => {
    const ticket = await Tickets.create({ title: 'Late order', description: '', owner: 'asha' });
    ticket.replies.push({ author: 'asha', message: 'Any update?' });
    ticket.replies.push({ author: 'neha', message: 'Arriving today' });
    await Tickets.save(ticket);

    const res = await request(app).get('/api/notifications/count').set(as('asha'));
    expect(res.body.count).toBe(1);
  });
});
