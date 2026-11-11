// In-memory "database" that behaves like Mongoose:
// every method is async and returns COPIES, so a change to a ticket
// is kept only after you call Tickets.save(ticket).

let tickets = [];
let nextId = 1;

const copy = (t) => (t ? { ...t, replies: t.replies.map((r) => ({ ...r })) } : null);

const Tickets = {
  async create(data) {
    const ticket = { id: nextId++, status: 'OPEN', replies: [], ...data };
    tickets.push(copy(ticket));
    return copy(ticket);
  },

  async findById(id) {
    return copy(tickets.find((t) => t.id === id));
  },

  async find(filter = {}) {
    return tickets
      .filter((t) => Object.entries(filter).every(([key, value]) => t[key] === value))
      .map(copy);
  },

  async save(ticket) {
    const index = tickets.findIndex((t) => t.id === ticket.id);
    tickets[index] = copy(ticket);
    return copy(ticket);
  },

  async deleteAll() {
    tickets = [];
    nextId = 1;
  },
};

module.exports = { Tickets };
