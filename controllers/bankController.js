const Bank = require('../models/bank');

const bank_index = (req, res) => {
  Bank.find().sort({ createdAt: -1 })
    .then(result => {
      res.render('index', { banks: result, title: 'All banks' });
    })
    .catch(err => {
      console.log(err);
    });
}

const bank_details = (req, res) => {
  const id = req.params.id;
  Bank.findById(id)
    .then(result => {
      res.render('details', { bank: result, title: 'Bank Details' });
    })
    .catch(err => {
      console.log(err);
    });
}

const bank_create_get = (req, res) => {
  res.render('create', { title: 'Create a new bank' });
}

const bank_create_post = (req, res) => {
  const bank = new Bank(req.body);
  bank.save()
    .then(result => {
      res.redirect('/banks');
    })
    .catch(err => {
      console.log(err);
    });
}

const bank_delete = (req, res) => {
  const id = req.params.id;
  Bank.findByIdAndDelete(id)
    .then(result => {
      res.json({ redirect: '/banks' });
    })
    .catch(err => {
      console.log(err);
    });
}

module.exports = {
  bank_index, 
  bank_details, 
  bank_create_get, 
  bank_create_post, 
  bank_delete
}