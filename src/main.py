from flask import Flask, request, render_template, redirect, make_response
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json

from utils.encoder import DateTimeEncoder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db/librarian.db')
db = SQLAlchemy(app)

from services.customer import CustomerService
from services.book import BookService
from services.bookunit import BookunitService
from services.rental import RentalService

@app.route('/')
def showIndex():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    loginObj = request.form
    username = loginObj.get('username')
    password = loginObj.get('password')

    if username == 'admin' and password == 'admin':
        resp = make_response(redirect(url_for('customerList')))
        resp.set_cookie('username', username)
        return resp

    return redirect(url_for('showIndex'))


@app.route('/book-search', methods = ['GET'])
def bookList():
    title = request.args.get('title', '')
    searchResults = BookService().search(title)
    return render_template('book-search.html', searchResults=searchResults, title=title)

@app.route('/rentals/add/<customerId>', methods = ['GET', 'POST'])
def addRentals(customerId):
    error = None
    customer = CustomerService().get(customerId)
    activeRentals = RentalService().listActiveForCustomer(customerId)
    historicRentals = RentalService().listHistoryForCustomer(customerId)

    if request.method == 'GET':
        return render_template('manage-rentals.html', customerId=customerId, cart=[], cartStr='[]', activeRentals=activeRentals, historicRentals=historicRentals, customer=customer)

    rentalObj = request.form
    barcode = rentalObj.get('barcode')

    cart = json.loads(rentalObj.get('cart', '[]'))

    try:
        cart = RentalService().addToRentalCart(customerId, barcode, cart)
    except Exception as e:
        error = e.args[0]
    finally:
        cart, totalCharge = RentalService().processCartForDisplay(cart)

    # cart, totalCharge = RentalService().processCartForDisplay(cart)
    cartStr = json.dumps(cart, cls=DateTimeEncoder)

    return render_template('manage-rentals.html', customerId=customerId, cart=cart, cartStr=cartStr, activeRentals=activeRentals, historicRentals=historicRentals, totalCharge=totalCharge, error=error)

@app.route('/rentals/confirm/<customerId>', methods = ['POST'])
def confirmRentals(customerId):
    rentalObj = request.form

    cart = json.loads(rentalObj.get('cart'))
    RentalService().create(cart)
    return redirect(url_for('addRentals', customerId=customerId))

@app.route('/manage-returns', methods = ['GET'])
def manageReturns():
    return render_template('handle-returns.html', cart=[], cartStr='[]')

@app.route('/returns/add', methods = ['POST'])
def addReturns():
    error = None
    rentalObj = request.form
    barcode = rentalObj.get('barcode')

    cart = json.loads(rentalObj.get('cart', '[]'))

    try:
        cart = RentalService().addToReturnCart( barcode, cart)
    except Exception as e:
        error = e.args[0]
    finally:
        cart, totalCharge = RentalService().processCartForDisplay(cart)

    cartStr = json.dumps(cart, cls=DateTimeEncoder)

    return render_template('handle-returns.html', cart=cart, cartStr=cartStr, totalCharge=totalCharge, error=error)

@app.route('/returns/confirm', methods = ['POST'])
def confirmReturns():
    rentalObj = request.form

    cart = json.loads(rentalObj.get('cart'))
    _, successMsg = RentalService().returnRentals(cart)
    return render_template('handle-returns.html', cart=[], cartStr='[]', successMsg=successMsg)

@app.route('/books', methods = ['GET'])
def bookSearch():
    return render_template('book-search.html')

@app.route('/books/<bookId>', methods = ['GET'])
def bookView(bookId):
    book = BookService().get(bookId)

    return render_template('view-book.html', book=book)

@app.route('/books/<bookId>/edit', methods = ['GET'])
def bookEdit(bookId):
    r = BookService().get(bookId)
    return render_template('edit-book.html', book=r)

@app.route('/books/add', methods = ['GET', 'POST'])
def bookAdd():
    if request.method == 'GET':
        return render_template('add-book.html', book=None)

    bookObj = request.form
    r = BookService().create(bookObj)
    return render_template('add-book.html', book=r)

@app.route('/book-unit/add', methods = ['POST'])
def bookunitAdd():
    bookunitObj = request.form
    bookId = bookunitObj.get('bookId')

    r = BookunitService().create(bookunitObj)

    return redirect(url_for('bookView', bookId=bookId))

@app.route('/book-unit/<bookId>/<bookunitId>/delete', methods = ['GET'])
def bookunitDelete(bookId, bookunitId):
    r = BookunitService().delete(bookunitId)

    return redirect(url_for('bookView', bookId=bookId))

@app.route('/books/outstanding', methods = ['GET'])
def outstandingBooks():
    outstandingRentals = RentalService().listAllActive()
    print(outstandingRentals)
    return render_template('outstanding-books.html', outstandingRentals=outstandingRentals)

@app.route('/customers', methods = ['GET'])
def customerList():
    r = CustomerService().listAll()
    return render_template('customer-search.html', customers=r)
@app.route('/customers/<customerId>', methods = ['GET'])
def customerView(customerId):
    r = CustomerService().get(customerId)
    return render_template('view-customer.html', customer=r)

@app.route('/customers/regnum', methods = ['GET'])
def customerViewByRegnum():
    regnum = request.args.get('regnum')
    r = CustomerService().getByRegnum(regnum)
    return render_template('customer-search.html', customers=r)
@app.route('/customers/<customerId>/edit', methods = ['GET', 'POST'])
def customerEdit(customerId):
    r = CustomerService().get(customerId)
    if request.method == 'GET':
        return render_template('edit-customer.html', customer=r, successMsg=None)

    customerObj = request.form
    successMsg = CustomerService().update(customerId, customerObj)
    return render_template('edit-customer.html', customer=r, successMsg=successMsg)

@app.route('/customers/add', methods = ['GET', 'POST'])
def customerAdd():
    if request.method == 'GET':
        return render_template('add-customer.html', customer=None)

    customerObj = request.form
    r = CustomerService().create(customerObj)
    return render_template('add-customer.html', customer=r)



@app.route('/api/v1/customer/create', methods = ['POST'])
def createCustomer():
    customerObj = request.json
    return CustomerService().create(customerObj)

@app.route('/api/v1/customer/<customerId>', methods = ['GET'])
def getCustomer(customerId):
    r = CustomerService().get(customerId)

    if r is None:
        return {}

    return r.to_dict()

@app.route('/api/v1/customer/<customerId>', methods = ['PUT'])
def updateCustomer(customerId):
    customerObj = request.json
    r = CustomerService().update(customerId, customerObj)
    return r

@app.route('/api/v1/customer/<customerId>', methods = ['DELETE'])
def deleteCustomer(customerId):
    r = CustomerService().delete(customerId)
    return r