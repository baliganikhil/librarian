from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime, Date, Text
from flask_sqlalchemy import SQLAlchemy

from main import db
from daos.basedao import BaseDAO
from models.rental import Rentals

meta = MetaData()

RentalStatus = {
    'RENTED': 'RENTED',
    'RETURNED': 'RETURNED'
}

class RentalDAO(BaseDAO):
    def __init__(self):
        super().__init__()

        print('Initialising rental dao')

    def insert(self, rental, commit=False):
        now = datetime.now()
        duedate = rental.get('duedate')
        duedate = datetime.strptime(duedate, '%Y-%m-%d %H:%M:%S.%f')

        rental = Rentals(
            bookunitId = rental.get('bookunitId'),
            customerId = rental.get('customerId'),
            duedate = duedate,
            charge = rental.get('charge'),
            status = rental.get('status'),
            comments = rental.get('comments'),
            createdat = now,
            updatedat = now,
            createdby = rental.get('createdby'),
            updatedby = rental.get('updatedby'),
        )

        db.session.add(rental)

        if commit == True:
            db.session.commit()

        return 'Rental has been created successfully'

    def listActiveForCustomer(self, customerId):
        rentals = Rentals.query.filter_by(customerId=customerId, status=RentalStatus.get('RENTED')).all()
        return rentals

    def listHistoryForCustomer(self, customerId):
        rentals = Rentals.query.filter_by(customerId=customerId, status=RentalStatus.get('RETURNED')).all()
        return rentals

    def delete(self, rentalId):
        rental = Rentals.query.get(rentalId)
        db.session.delete(rental)
        db.session.commit()
        return 'Rental has been deleted successfully'

    def markReturned(self, rentalIds):
        rows = Rentals.query.filter(Rentals.id.in_(rentalIds)).all()
        for row in rows:
            row.status = RentalStatus.get('RETURNED')

        db.session.commit()
        return 'Rentals marked successfully as returned'

    def getRentalForReturn(self, bookunitId):
        rental = Rentals.query.filter_by(bookunitId=bookunitId, status=RentalStatus.get('RENTED')).first()
        return rental
