from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime, Date, Text
from flask_sqlalchemy import SQLAlchemy

from main import db
from daos.basedao import BaseDAO
from models.book import Books

meta = MetaData()

class BookDAO(BaseDAO):
    def __init__(self):
        super().__init__()

        print('Initialising book dao')

    def insert(self, book):
        now = datetime.now()

        book = Books(
            title = book.get('title'),
            isbn13 = book.get('isbn13'),
            isbn10 = book.get('isbn10'),
            isbn = book.get('isbn'),
            author = book.get('author'),
            publisher = book.get('publisher'),
            language = book.get('language'),
            binding = book.get('binding'),
            numpages = book.get('numpages'),
            description = book.get('description'),
            charge = book.get('charge'),
            rentduration = book.get('rentduration'),
            createdat = now,
            updatedat = now,
            createdby = book.get('createdby'),
            updatedby = book.get('updatedby'),
        )

        db.session.add(book)
        db.session.commit()
        return 'Book has been created successfully'

    def get(self, bookId):
        book = Books.query.filter_by(id=bookId).first()
        return book

    def update(self, customerId, customerObj):
        now = datetime.now()

        book = Books.query.get(customerId)

        book.title = customerObj.get('title')
        book.isbn13 = customerObj.get('isbn13')
        book.isbn10 = customerObj.get('isbn10')
        book.isbn = customerObj.get('isbn')
        book.author = customerObj.get('author')
        book.publisher = customerObj.get('publisher')
        book.language = customerObj.get('language')
        book.binding = customerObj.get('binding')
        book.numpages = customerObj.get('numpages')
        book.description = customerObj.get('description')
        book.charge = customerObj.get('charge')
        book.rentduration = customerObj.get('rentduration')
        book.updatedat = now
        book.createdby = customerObj.get('createdby')
        book.updatedby = customerObj.get('updatedby')

        db.session.commit()
        return 'Book has been updated successfully'

    def delete(self, bookId):
        book = Books.query.get(bookId)
        db.session.delete(book)
        db.session.commit()
        return 'Book has been deleted successfully'

    def search(self, title):
        return Books.query.filter(Books.title.ilike(f'%{title}%')).all()