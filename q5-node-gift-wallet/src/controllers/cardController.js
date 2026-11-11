const { Cards } = require('../data/store');
const { HttpError } = require('../utils/httpError');

async function listCards(req, res) {
  res.json(await Cards.findAll());
}

async function addCard(req, res) {
  const { code, balance } = req.body;
  if (!code || typeof balance !== 'number' || balance <= 0) {
    throw new HttpError(400, 'code and a positive balance are required');
  }
  if (Cards.existsByCode(code)) {
    throw new HttpError(409, 'This card is already in your wallet');
  }
  const card = await Cards.create({ code, balance });
  res.status(201).json(card);
}

async function getCard(req, res) {
  const card = await Cards.findById(req.params.id);
  if (!card) {
    throw new HttpError(404, 'Card not found');
  }
  res.json(card);
}

async function spend(req, res) {
  const card = await Cards.findById(Number(req.params.id));
  if (!card) {
    throw new HttpError(404, 'Card not found');
  }
  const { amount } = req.body;
  if (typeof amount !== 'number' || amount <= 0) {
    throw new HttpError(400, 'amount must be a positive number');
  }
  if (amount > card.balance) {
    throw new HttpError(400, 'Not enough balance');
  }
  card.balance -= amount;
  res.json(await Cards.save(card));
}

module.exports = { listCards, addCard, getCard, spend };
