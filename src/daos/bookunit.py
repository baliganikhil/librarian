from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime, Date, Text
from flask_sqlalchemy import SQLAlchemy

from main import db
from daos.basedao import BaseDAO
from models.bookunit import Bookunits

meta = MetaData()

class BookunitDAO(BaseDAO):
    def __init__(self):
        super().__init__()

        print('Initialising book unit dao')

    def get(self, bookunitId):
        bookunit = Bookunits.query.filter_by(id=bookunitId).first()
        return bookunit

    def insert(self, bookunit):
        now = datetime.now()

        bookunit = Bookunits(
            barcode = bookunit.get('barcode'),
            bookId = bookunit.get('bookId'),
            createdat = now,
            updatedat = now,
            createdby = bookunit.get('createdby'),
            updatedby = bookunit.get('updatedby'),
        )

        db.session.add(bookunit)
        db.session.commit()
        return 'Book Unit has been created successfully'

    def list(self, bookId):
        bookunits = Bookunits.query.filter_by(bookId=bookId).all()
        return bookunits

    def getByBarcode(self, barcode):
        bookunit = Bookunits.query.filter_by(barcode=barcode).first()
        return bookunit

    def delete(self, bookunitId):
        bookunit = Bookunits.query.get(bookunitId)
        db.session.delete(bookunit)
        db.session.commit()
        return 'Book Unit has been deleted successfully'