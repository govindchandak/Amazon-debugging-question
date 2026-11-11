const express = require('express');
const classRoutes = require('./routes/classRoutes');
const { requireMember } = require('./middleware/auth');
const { errorHandler } = require('./middleware/errorHandler');

const app = express();

app.use(express.json());
app.use('/api', requireMember);
app.use('/api/classes', classRoutes);
app.use(errorHandler);

module.exports = app;
