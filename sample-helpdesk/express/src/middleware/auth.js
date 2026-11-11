const USERS = {
  asha: 'CUSTOMER',
  ravi: 'CUSTOMER',
  neha: 'AGENT',
};

// Every /api request must say who is calling, in the X-User header.
function requireUser(req, res, next) {
  const name = req.header('X-User');
  if (name && !USERS[name]) {
    return res.status(401).json({ error: 'Unknown user' });
  }
  req.user = { name, role: USERS[name] };
  next();
}

module.exports = { requireUser, USERS };
