const { Tickets } = require('../data/store');
const { HttpError } = require('../utils/httpError');

const PAGE_SIZE = 5;
const STATUSES = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'];

const summary = (t) => ({ id: t.id, title: t.title, owner: t.owner, status: t.status });

async function createTicket(title, description, user) {
  const ticket = await Tickets.create({ title, description, owner: user.name });
  return summary(ticket);
}

// Customers see only their own tickets. Agents see all. Newest first, 5 per page.
async function listTickets(user, page) {
  const filter = user.role === 'AGENT' ? {} : { owner: user.name };
  const all = await Tickets.find(filter);
  all.sort((a, b) => b.id - a.id);
  const start = page * PAGE_SIZE;
  return all.slice(start, start + PAGE_SIZE).map(summary);
}

// Loads a ticket the user is allowed to see.
async function findVisibleTicket(id, user) {
  const ticket = await Tickets.findById(id);
  return ticket;
}

async function getTicket(id, user) {
  const ticket = await findVisibleTicket(id, user);
  return { ...summary(ticket), description: ticket.description, replies: ticket.replies };
}

async function addReply(id, message, user) {
  const ticket = await findVisibleTicket(id, user);
  if (!message || !message.trim()) {
    throw new HttpError(400, 'Message is required');
  }
  const reply = { author: user.name, message: message.trim() };
  ticket.replies.push(reply);
  return reply;
}

async function changeStatus(id, newStatus, user) {
  if (user.role !== 'AGENT') {
    throw new HttpError(403, 'Only agents can change status');
  }
  if (!STATUSES.includes(newStatus)) {
    throw new HttpError(400, `Status must be one of ${STATUSES.join(', ')}`);
  }
  const ticket = await Tickets.findById(id);
  if (!ticket) {
    throw new HttpError(404, 'Ticket not found');
  }
  ticket.status = newStatus;
  await Tickets.save(ticket);
  return summary(ticket);
}

// How many replies on my tickets were written by someone else.
async function countRepliesFromOthers(user) {
  const mine = await Tickets.find({ owner: user.name });
  return mine.reduce((count, ticket) => count + ticket.replies.length, 0);
}

module.exports = { createTicket, listTickets, getTicket, addReply, changeStatus, countRepliesFromOthers };
