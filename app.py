import code
from itertools import product
import os
from os import path
import secrets
from flask import Flask, url_for, redirect, request, flash, session
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, login_required, LoginManager, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime
from werkzeug.utils import secure_filename
import random
import string


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))



class ProductsInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer)
    dateaddes = db.Column(db.DateTime, default=datetime.utcnow)
    imageName = db.Column(db.Text, nullable=True)
    seller= db.Column(db.String(200), nullable=False)



    def __repr__(self):
        return f'<Task : {self.id}>'


class Transaction(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), nullable=False,)
    receiver = db.Column(db.String(80))
    amount = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    mobile = db.Column(db.String(20), nullable=False, unique=True)

class Bankuser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    secret = db.Column(db.String(20), nullable=False, unique=True)
    balance=db.Column(db.Integer,nullable=False)



class RegsiterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    email = EmailField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Email"})
    mobile = StringField(validators=[InputRequired(), Length(
        min=10, max=15)], render_kw={"placeholder": "Mobile no."})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    password2 = PasswordField(validators=[InputRequired(), ],
                              render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Register")

    def validate_user(self, username, email, mobile):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'User already exists. Please choose a different username.')

        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                'User already exists. Please choose a different email.')

        existing_user_mobile = User.query.filter_by(mobile=mobile.data).first()
        if existing_user_mobile:
            raise ValidationError(
                'User already exists. Please choose a different mobile number.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --------------------------------> Admin Homepage
@app.route('/admin', methods=['GET', 'POST'])
def adminHome():
    if 'username' in session and session['username'] == 'admin':
        # --------------> For admin to add new product
        if request.method == 'POST':
            image = request.files['productImage']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            newItem = ProductsInfo(
                name=request.form['productName'],
                author=request.form['productAuthor'],
                description=request.form['productDescription'],
                price=request.form['productPrice'],
                seller=request.form['productSeller'],
                imageName=image.filename
            )
            # new_seller=Seller(
            #     id=34,
            #     username=request.form['productSeller'],
            #     balance=1000
            # )
            # db.session.add(new_seller)
            # db.session.commit()
            try:
                session['productName'] = request.form['productName']
                db.session.add(newItem)
                db.session.commit()
                flash(f'Product added successfully', 'success')
                return redirect('/admin')
            except:
                return "There was an issue pushing to database"

        # --------------------> For admin to display all the stored products
        else:
            products = ProductsInfo.query.order_by(ProductsInfo.name).all()
            return render_template('Admin/adminPanel.html', products=products)
    else:
        return render_template('Error.html', title='Access Denied', msg="Unable to access admin Homepage. Please signin to continue.")






# -------------------------> User Homepage
@app.route('/buying/<name>', methods=['GET', 'POST'])
def buying(name):
    print(session['username'])
    buyer=session['username']
    print(buyer)
    buyer_account=Bankuser.query.filter_by(username = buyer).all()
    book_to_buy=ProductsInfo.query.filter_by(name = name).all()
    print(buyer_account[0].balance)
    print(book_to_buy[0].price)
    if request.method == 'POST':
        amount=request.form.get('select1')
    print(amount)
    if (int(buyer_account[0].balance)> (int(amount)*int(book_to_buy[0].price))):
        print("YES")
        print(session)
        product=book_to_buy[0].id
        amount=int(amount)
    
        seller=book_to_buy[0].seller
        return redirect(url_for('bank', product=product,amount=amount,seller=seller,buyer=buyer))
    else:
        return render_template("no_balance.html")
    
@app.route('/bank', methods=['GET', 'POST'])
def bank():
    # x=Bankuser.query.all()
    # for i in x:
    #     print(i.id)
    #     print(i.username)
    #     print(i.balance)
    product=request.args.get('product')
    amount=request.args.get('amount')
    seller=request.args.get('seller')
    buyer=request.args.get('buyer')
    book_to_buy=ProductsInfo.query.filter_by(id = int(product)).all()
    buyer_account=Bankuser.query.filter_by(username = buyer).all()
    print(book_to_buy[0])
    print(buyer_account[0])

    now_balance_buyer=buyer_account[0].balance
    id=buyer_account[0].id
    account_update=Bankuser.query.get_or_404(id)
    account_update.balance=int(now_balance_buyer)-(int(amount)*int(book_to_buy[0].price))

    reduce_balance_buyer=int(now_balance_buyer)-(int(amount)*int(book_to_buy[0].price))
    book_to_buy[0].balance=reduce_balance_buyer
    print(reduce_balance_buyer)
    db.session.commit()
    ecommerce=Bankuser.query.get_or_404(100)
    prev=ecommerce.balance
    ecommerce.balance=int(prev)+(int(amount)*int(book_to_buy[0].price))
    db.session.commit()

    
    letters = string.digits
    x=int(''.join(random.choice(letters) for i in range(5)))
    new_transaction=Transaction(
        id=x,
        sender=buyer,
        receiver='bank',
        amount=(int(amount)*int(book_to_buy[0].price))
    ) 
    db.session.add(new_transaction)
    db.session.commit()
    
    




    
    return  redirect(url_for('seller',x=x,seller=seller))
        

@app.route('/seller')
def seller():
    transaction_id=int(request.args.get('x'))
    sell=request.args.get('seller')
    seller=Bankuser.query.filter_by(username = sell).all()
    print(seller[0])
    print(sell)
    transaction=Transaction.query.get_or_404(transaction_id)
    ecommerce=Bankuser.query.get_or_404(100)
    amount=int(transaction.amount)
    # print(amount)
    old_balance_ecommerce=ecommerce.balance
    ecommerce.balance=old_balance_ecommerce-amount
    sellerid=seller[0].id
    seller1=Bankuser.query.get_or_404(sellerid)
    old_balance_seller=seller1.balance
    seller1.balance=old_balance_seller+amount
    db.session.commit()
    
    
    return render_template('bank.html')


@app.route('/',methods=['POST', 'GET'])
def home():
    y=Bankuser.query.all()
    print(y)
    for i in y:
        print(i.id)
        print(i.username)
        print(i.balance)
    x=Transaction.query.all()
    print("--------------------------------")
    for i in x:
        print(i.id)
        print(i.sender)
        print(i.receiver)
        print(i.amount)
    print("--------------------------------")
    z= Bankuser.query.all()
    for i in z:
        print(i.id)
        print(i.username)
        print(i.secret)


    
    if not path.exists("database.db"):
        db.create_all()
        new_seller=Bankuser(
            id=11,
            username='seller1',
            secret='abcd1',
            balance=1000
        )
        new_seller2=Bankuser(
            id=12,
            username='seller2',
            secret='abcd2',
            balance=1000
        )
        new_seller3=Bankuser(
            id=13,
            username='seller3',
            secret='abcd3',
            balance=1000
        )
        db.session.add(new_seller)
        db.session.add(new_seller2)
        db.session.add(new_seller3)
        db.session.commit()
        
        
    allProducts = []
    # print(session)
    # Adding a username in session with value if doesn't exists any.
    if 'username' not in session:
        session['username'] = 'None'
        session['logged_in'] = False

    try:
        allProducts = ProductsInfo.query.all()
    except:
        pass
    if 'username' in session:
        # print(Bankuser.query.get(5))
        if (len(Bankuser.query.filter_by(username = session['username']).all()))==0 and session['username']!='None':
            return render_template('/bankuser.html')
        # resp=Bankuser.query.all()
        # print(resp[0].username)
        # print(session)
        # print(session['username'])
    return render_template('home.html', allProducts=allProducts)


# -----------------------------> For logging in admin and normal users
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Adding a username in session with value if doesn't exists any.
    if 'username' not in session:
        session['username'] = 'None'
        session['logged_in'] = False


    form = LoginForm()
    # For admin
    if form.username.data and form.username.data == 'admin':
        if form.password.data == 'admin':
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect('/admin')
        else:
            flash(f'Your credentials did not match. Please try again', 'danger')
            return redirect('/login')

    # For normal user
    else:
        if form.validate_on_submit():
            username = User.query.filter_by(
                username=form.username.data).first()
            if username:
                if bcrypt.check_password_hash(username.password, form.password.data):
                    session['username'] = request.form['username']
                    session['logged_in'] = True
                    login_user(username)
                    return redirect('/')
                else:
                    flash(f'Your credentials did not match. Please try again', 'danger')
                    return redirect(url_for('login'))
            else:
                flash(f'Your credentials did not match. Please try again', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)


# ---------------------------------> For Logging Out Users
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    session['username'] = 'None'
    session['logged_in'] = False
    return redirect(url_for('login'))

# -----------------------------------> For signing up a user


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegsiterForm()
    if form.validate_on_submit():
        if (form.username.data).lower() == 'admin' or (form.username.data).lower() == 'none':
            flash(f'Username not allowed. Please any other username.', 'danger')
            return redirect(url_for('signup'))
        elif (form.password.data != form.password2.data):
            flash(f'Password mismatch.', 'danger')

        else:
            try:
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data, 12)
                new_user = User(username=form.username.data, password=hashed_password,
                                email=form.email.data, mobile=form.mobile.data)
                db.session.add(new_user)
                db.session.commit()
                flash(f'You have signed up successfully. Please login now.', 'success')
                return redirect(url_for('login'))
            except:
                # return render_template('Error.html', title="Integrity Voilation")
                flash(f'User with same details already exists.', 'danger')
                return redirect(url_for('signup'))

    return render_template('register.html', form=form)


# ----------------------------------------> Buying a book
@app.route('/order/<int:productid>')
def order(productid):
    if 'username' in session and session['username'] != 'None':
        try:
            productDetails = ProductsInfo.query.get_or_404(productid)
            print(productDetails.imageName)
            return render_template('order.html', productDetails=productDetails)
        except:
            #!!! Product not found Warning must show up
            return redirect('/')
    else:
        flash(f'To buy, you need to be signed up!', 'danger')
        return redirect('/login')
@app.route('/add', methods=['POST', 'GET'])
def add():
    return render_template('/bankuser.html')

@app.route('/add_bankuser', methods=['POST'])
def add_bankuser():
    if request.method == 'POST':
        id = request.form['ID']
        name = request.form['name']

        secret = request.form['secret']
    
        new_bank_user = Bankuser(id=id,
                        username=name,
                        secret=secret,
                        balance=1000
                        )
        db.session.add(new_bank_user)
        db.session.commit()
        return render_template('home.html')
    
@app.route('/checkbalance',methods=['GET', 'POST'])
def checkbalance():



    return render_template('check.html')

@app.route('/check_account',methods=['GET', 'POST'])
def check_account():
    if request.method == 'POST':
        id = request.form['ID']
        secret = request.form['secret']
        user=Bankuser.query.get_or_404(id)
    if secret==user.secret:
        balance=user.balance
        holder=user.username
    else:
        flash(f'Keys Didnt Match!', 'danger')
        return redirect('/checkbalance')
        


    return render_template('balance.html',balance=balance,id=id,holder=holder)

def getApp():
    return app


if __name__ == '__main__':
    app.run(debug=True)
