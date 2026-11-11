const app = require('./app');

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`HelpDesk running on http://localhost:${PORT}`));
