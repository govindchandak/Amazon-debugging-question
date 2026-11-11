const service = require('../services/ticketService');

async function countNew(req, res) {
  res.json({ count: await service.countRepliesFromOthers(req.user) });
}

module.exports = { countNew };
