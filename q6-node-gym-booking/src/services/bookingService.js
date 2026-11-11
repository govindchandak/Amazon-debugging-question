const { Classes } = require('../data/store');
const { HttpError } = require('../utils/httpError');

async function findClass(id) {
  const gymClass = await Classes.findById(id);
  if (!gymClass) {
    throw new HttpError(404, 'Class not found');
  }
  return gymClass;
}

// Books a seat, or puts the member on the waitlist when the class is full.
async function book(id, member) {
  const gymClass = await findClass(id);
  if (gymClass.booked.includes(member)) {
    throw new HttpError(409, 'You already have a place in this class');
  }
  let status;
  if (gymClass.booked.length > gymClass.capacity) {
    gymClass.waitlist.push(member);
    status = 'WAITLISTED';
  } else {
    gymClass.booked.push(member);
    status = 'BOOKED';
  }
  await Classes.save(gymClass);
  return { classId: gymClass.id, member, status };
}

// Cancels a booking. The first person on the waitlist gets the free seat.
async function cancel(id, member) {
  const gymClass = await findClass(id);
  const seat = gymClass.booked.indexOf(member);
  const waiting = gymClass.waitlist.indexOf(member);

  if (seat !== -1) {
    gymClass.booked.splice(seat, 1);
    if (gymClass.waitlist.length > 0) {
      gymClass.booked.push(gymClass.waitlist.pop());
    }
  } else if (waiting !== -1) {
    gymClass.waitlist.splice(waiting, 1);
  } else {
    throw new HttpError(404, 'You have no booking in this class');
  }
  await Classes.save(gymClass);
  return { classId: gymClass.id, member, status: 'CANCELLED' };
}

module.exports = { findClass, book, cancel };
