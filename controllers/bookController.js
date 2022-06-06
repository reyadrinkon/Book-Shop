const Book = require('../models/book');

const book_index = (req, res) => {
  Book.find().sort({ createdAt: -1 })
    .then(result => {
      res.render('index', { books: result, title: 'All books' });
    })
    .catch(err => {
      console.log(err);
    });
}

const book_details = (req, res) => {
  const id = req.params.id;
  Book.findById(id)
    .then(result => {
      res.render('details', { book: result, title: 'Book Details' });
    })
    .catch(err => {
      console.log(err);
    });
}

const book_create_get = (req, res) => {
  res.render('create', { title: 'Create a new book' });
}

const book_create_post = (req, res) => {
  const book = new Book(req.body);
  book.save()
    .then(result => {
      res.redirect('/books');
    })
    .catch(err => {
      console.log(err);
    });
}

const book_delete = (req, res) => {
  const id = req.params.id;
  Book.findByIdAndDelete(id)
    .then(result => {
      res.json({ redirect: '/books' });
    })
    .catch(err => {
      console.log(err);
    });
}

module.exports = {
  book_index, 
  book_details, 
  book_create_get, 
  book_create_post, 
  book_delete
}