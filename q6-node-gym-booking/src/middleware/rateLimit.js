// Each member may send at most 5 booking requests (book or cancel) per minute.
const LIMIT = 5;
const WINDOW_MS = 60 * 1000;

let hits = new Map(); // key -> list of request times

function bookingLimiter(req, res, next) {
  const key = req.ip;
  const now = Date.now();
  const recent = (hits.get(key) || []).filter((time) => now - time < WINDOW_MS);
  if (recent.length >= LIMIT) {
    return res.status(429).json({ error: 'Too many booking requests. Try again in a minute.' });
  }
  recent.push(now);
  hits.set(key, recent);
  next();
}

function resetLimits() {
  hits = new Map();
}

module.exports = { bookingLimiter, resetLimits };
