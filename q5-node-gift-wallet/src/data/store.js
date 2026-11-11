// In-memory "database" that behaves like Mongoose:
// every method is async (returns a Promise) and returns copies.

let cards = [];
let nextId = 1;

const copy = (c) => (c ? { ...c } : null);

const Cards = {
  async create(data) {
    const card = { id: nextId++, ...data };
    cards.push(copy(card));
    return copy(card);
  },

  async findAll() {
    return cards.map(copy);
  },

  async findById(id) {
    return copy(cards.find((c) => c.id === id));
  },

  async existsByCode(code) {
    return cards.some((c) => c.code === code);
  },

  async save(card) {
    const index = cards.findIndex((c) => c.id === card.id);
    cards[index] = copy(card);
    return copy(card);
  },

  async deleteAll() {
    cards = [];
    nextId = 1;
  },
};

module.exports = { Cards };
