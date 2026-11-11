const express = require('express');
const tickets = require('../controllers/ticketController');

const router = express.Router();

router.post('/', tickets.createTicket);
router.get('/', tickets.listTickets);
router.get('/:id', tickets.getTicket);
router.post('/:id/reply', tickets.addReply);
router.patch('/:id/status', tickets.changeStatus);

module.exports = router;
