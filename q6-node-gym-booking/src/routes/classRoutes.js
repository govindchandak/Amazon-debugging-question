const express = require('express');
const classes = require('../controllers/classController');
const { bookingLimiter } = require('../middleware/rateLimit');

const router = express.Router();

router.get('/:id', classes.getClass);
router.post('/:id/book', bookingLimiter, classes.book);
router.delete('/:id/book', bookingLimiter, classes.cancel);
router.get('/:id/attendees', classes.attendees);

module.exports = router;
