// In-memory "database" that behaves like Mongoose:
// every method is async and returns copies. Call save() to keep a change.

let classes = [];
let nextId = 1;

const copy = (c) => (c ? { ...c, booked: [...c.booked], waitlist: [...c.waitlist] } : null);

const Classes = {
  async create(data) {
    const gymClass = { id: nextId++, booked: [], waitlist: [], ...data };
    classes.push(copy(gymClass));
    return copy(gymClass);
  },

  async findById(id) {
    return copy(classes.find((c) => c.id === id));
  },

  async save(gymClass) {
    const index = classes.findIndex((c) => c.id === gymClass.id);
    classes[index] = copy(gymClass);
    return copy(gymClass);
  },

  async deleteAll() {
    classes = [];
    nextId = 1;
  },
};

module.exports = { Classes };
