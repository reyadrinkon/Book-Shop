const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const bankSchema = new Schema({
  ac_holder: {
    type: String,
    required: true,
  },
  ac_id: {
    type: String,
    required: true,
  },
  balance: {
    type: Number,
    required: true
  },
}, { timestamps: true });

const Bank = mongoose.model('Bank', bankSchema);
module.exports = Bank;