const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');
const bookRoutes = require('./routes/bookRoutes');
const Book=require('./models/book')

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
    title:'book1',
    snippet:'hsdjfkjdh',
    body:'sdhjksh'

  })
  book.save()
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

// 404 page
app.use((req, res) => {
  res.status(404).render('404', { title: '404' });
});