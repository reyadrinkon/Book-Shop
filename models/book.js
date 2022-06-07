const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const bookSchema = new Schema({
  title: {
    type: String,
    required: true,
  },
  Vendor: {
    type: String,
    required: true,
  },
  quantity_available: {
    type: Number,
    required: true
  },
  price: {
    type: Number,
    required: true
  },
}, { timestamps: true });

const Book = mongoose.model('Book', bookSchema);
module.exports = Book;