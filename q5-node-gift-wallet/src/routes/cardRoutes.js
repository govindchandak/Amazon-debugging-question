const express = require('express');
const cards = require('../controllers/cardController');

const router = express.Router();

router.get('/', cards.listCards);
router.post('/', cards.addCard);
router.get('/:id', cards.getCard);
router.post('/:id/spend', cards.spend);

module.exports = router;
