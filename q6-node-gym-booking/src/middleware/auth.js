const MEMBERS = {
  asha: 'MEMBER',
  ravi: 'MEMBER',
  kiran: 'MEMBER',
  neha: 'TRAINER',
};

function requireMember(req, res, next) {
  const name = req.header('X-Member');
  if (!name || !MEMBERS[name]) {
    return res.status(401).json({ error: 'Send a valid X-Member header' });
  }
  req.member = { name, role: MEMBERS[name] };
  next();
}

module.exports = { requireMember };
