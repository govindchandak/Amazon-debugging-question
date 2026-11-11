const express = require('express');
const cardRoutes = require('./routes/cardRoutes');
const { errorHandler } = require('./middleware/errorHandler');

const app = express();

app.use('/api/cards', cardRoutes);
app.use(express.json());
app.use(errorHandler);

module.exports = app;
