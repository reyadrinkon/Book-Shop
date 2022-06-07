const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');
const bookRoutes = require('./routes/bookRoutes');
const bankRoutes = require('./routes/bankRoutes');
const Book=require('./models/book')
const Bank=require('./models/bank')
const {MongoClient} = require('mongodb');

const dbURI = "mongodb+srv://rinkon:rinkon123@cluster0.vwseqcq.mongodb.net/book-shop?retryWrites=true&w=majority";



// express app
const app = express();

// connect to mongodb & listen for requests

mongoose.connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(result => app.listen(3000))
  .catch(err => console.log(err));

// register view engine
app.set('view engine', 'ejs');

// middleware & static files
app.use(express.static('public'));
app.use(express.json())
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));
app.use((req, res, next) => {
  res.locals.path = req.path;
  next();
});
const updateInDB=async()=>{
  let data=await Book.updateOne(
    {name: "thebok2"},
    {$set:{price:10}}
  )
  console.log(data)
}
// routes
app.get('/', async(req, res) => {
  res.redirect('/books');
});
app.post('/', (req, res) => {
 // console.log(Book.find())

//  console.log(req.body)
  


  const book= new Book({
    title:req.body.title,
    Author:req.body.Author,
    quantity_available:req.body.quantity_available,
    price:req.body.price

  })
  book.save()
    .then((result)=>{
      //updateInDB()
 
      res.send(result)
    })
    .catch((err)=>{
      console.log(err)
    })
})
app.get('/createaccount', (req, res) => {
  res.redirect('/banks');
});
app.post('/createaccount', (req, res) => {
  const x=Bank.find()
  console.log(db.Bank)
  const bank= new Bank({
    ac_holder:req.body.ac_holder,
    ac_id:req.body.ac_id,
    balance:req.body.balance

  })
  bank.save()
    .then((result)=>{
      res.send(result)
    })
    .catch((err)=>{
      console.log(err)
    })
})

app.get('/about', (req, res) => {
  res.render('about', { title: 'About' });
});

// book routes
app.use('/books', bookRoutes);
app.use('/banks', bankRoutes);


// 404 page
app.use((req, res) => {
  res.status(404).render('404', { title: '404' });
});
