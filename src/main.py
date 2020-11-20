from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db/librarian.db')
db = SQLAlchemy(app)

from services.customer import CustomerService
from services.book import BookService

@app.route('/')
def hello_world():
    r = CustomerService().get(1)
    print(r)
    print(r.name)

    # print(r.fetchall())
    # print(dir(r))
    return 'Hello, World!'

@app.route('/book-search', methods = ['GET'])
def bookList():
    return render_template('book-search.html')

@app.route('/manage-rentals/<customerId>', methods = ['GET'])
def manageRentals(customerId):
    return render_template('manage-rentals.html')

@app.route('/manage-returns', methods = ['GET'])
def manageReturns():
    return render_template('handle-returns.html')

@app.route('/books', methods = ['GET'])
def bookSearch():
    return render_template('book-search.html')

@app.route('/books/<bookId>', methods = ['GET'])
def bookView(bookId):
    r = BookService().get(bookId)
    return render_template('view-book.html', book=r)

@app.route('/books/<bookId>/edit', methods = ['GET'])
def bookEdit(bookId):
    r = BookService().get(bookId)
    return render_template('edit-book.html', book=r)

@app.route('/books/add', methods = ['GET'])
def bookAdd():
    return render_template('add-book.html')

@app.route('/books/outstanding', methods = ['GET'])
def outstandingBooks():
    return render_template('outstanding-books.html')

@app.route('/customers', methods = ['GET'])
def customerList():
    r = CustomerService().get(1)
    return render_template('customer-search.html', customer=r)
@app.route('/customers/<customerId>', methods = ['GET'])
def customerView(customerId):
    r = CustomerService().get(customerId)
    return render_template('view-customer.html', customer=r)

@app.route('/customers/<customerId>/edit', methods = ['GET'])
def customerEdit(customerId):
    r = CustomerService().get(customerId)
    return render_template('edit-customer.html', customer=r)

@app.route('/customers/add', methods = ['GET'])
def customerAdd():
    return render_template('add-customer.html')



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