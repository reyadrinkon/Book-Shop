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


const mongo = require('mongodb');

const MongoClient = mongo.MongoClient;

const url = "mongodb+srv://rinkon:rinkon123@cluster0.vwseqcq.mongodb.net/book-shop?retryWrites=true&w=majority";
MongoClient.connect(url, { useNewUrlParser: true }, (err, client) => {

    if (err) throw err;

    const db = client.db("book-shop");

    db.collection('books').updateOne({title:"thebook2"},{$inc:{price:-2}})
    db.collection('books').find({title:"thebook2"}).toArray().then((docs) => {

        console.log(docs);

    }).catch((err) => {

        console.log(err);
    }).finally(() => {

        client.close();
    });
});
const Bank = mongoose.model('Bank', bankSchema);
module.exports = Bank;