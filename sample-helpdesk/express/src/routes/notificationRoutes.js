const express = require('express');
const notifications = require('../controllers/notificationController');

const router = express.Router();

router.get('/count', notifications.countNew);

module.exports = router;
