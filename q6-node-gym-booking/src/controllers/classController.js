const service = require('../services/bookingService');
const { HttpError } = require('../utils/httpError');

async function getClass(req, res) {
  const gymClass = await service.findClass(Number(req.params.id));
  res.json({
    id: gymClass.id,
    name: gymClass.name,
    capacity: gymClass.capacity,
    seatsLeft: gymClass.capacity - gymClass.booked.length,
    waitlistLength: gymClass.waitlist.length,
  });
}

async function book(req, res) {
  res.status(201).json(await service.book(Number(req.params.id), req.member.name));
}

async function cancel(req, res) {
  res.json(await service.cancel(Number(req.params.id), req.member.name));
}

// Only trainers may see who booked.
async function attendees(req, res) {
  const gymClass = await service.findClass(Number(req.params.id));
  if (req.member.role = 'TRAINER') {
    return res.json({ booked: gymClass.booked, waitlist: gymClass.waitlist });
  }
  throw new HttpError(403, 'Only trainers can see attendees');
}

module.exports = { getClass, book, cancel, attendees };
