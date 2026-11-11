const express = require('express');
const ticketRoutes = require('./routes/ticketRoutes');
const notificationRoutes = require('./routes/notificationRoutes');
const { requireUser } = require('./middleware/auth');
const { errorHandler } = require('./middleware/errorHandler');

const app = express();

app.use(express.json());
app.use('/api', requireUser);
app.use('/api/tickets', ticketRoutes);
app.use('/api/notifications', notificationRoutes);
app.use(errorHandler);

module.exports = app;
