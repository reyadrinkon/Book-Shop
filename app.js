const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');
const bookRoutes = require('./routes/bookRoutes');
const bankRoutes = require('./routes/bankRoutes');

const Book=require('./models/book')
const Bank=require('./models/bank')


// express app
const app = express();

// connect to mongodb & listen for requests
const dbURI = "mongodb+srv://rinkon:rinkon123@cluster0.vwseqcq.mongodb.net/book-shop?retryWrites=true&w=majority";


mongoose.connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(result => app.listen(3000))
  .catch(err => console.log(err));

// register view engine
app.set('view engine', 'ejs');

// middleware & static files
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));
app.use((req, res, next) => {
  res.locals.path = req.path;
  next();
});

// routes
app.get('/', (req, res) => {
  res.redirect('/books');
});
app.post('/', (req, res) => {
  const book= new Book({
    title:'book2',
    Author:'rinkon',
    quantity_available: 50,
    price:23

  })
  book.save()
    .then((result)=>{
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
  const bank= new Bank({
    ac_holder:'rinkon',
    ac_id:'123',
    balance:50

  })
  bank.save()
    .then((result)=>{
      console.log(req.body)
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