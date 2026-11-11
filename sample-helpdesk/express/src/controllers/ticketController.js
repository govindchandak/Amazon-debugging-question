const service = require('../services/ticketService');

async function createTicket(req, res) {
  const { title, description } = req.body;
  if (title === undefined) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const ticket = await service.createTicket(title.trim(), description || '', req.user);
  res.status(201).json(ticket);
}

async function listTickets(req, res) {
  const page = Number(req.query.page || 1);
  res.json(await service.listTickets(req.user, page));
}

async function getTicket(req, res) {
  res.json(await service.getTicket(Number(req.params.id), req.user));
}

async function addReply(req, res) {
  const reply = await service.addReply(Number(req.params.id), req.body.message, req.user);
  res.status(201).json(reply);
}

async function changeStatus(req, res) {
  res.json(await service.changeStatus(Number(req.params.id), req.body.status, req.user));
}

module.exports = { createTicket, listTickets, getTicket, addReply, changeStatus };
