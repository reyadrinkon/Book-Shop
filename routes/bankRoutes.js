const express = require('express');
const bankController = require('../controllers/bankController');

const router = express.Router();

router.get('/create', bankController.bank_create_get);
router.get('/', bankController.bank_index);
router.post('/', bankController.bank_create_post);
router.get('/:id', bankController.bank_details);
router.delete('/:id', bankController.bank_delete);

module.exports = router;