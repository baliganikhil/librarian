from datetime import datetime
import re
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime, Date, Text
from flask_sqlalchemy import SQLAlchemy

from main import db
from daos.basedao import BaseDAO
from models.customer import Customers
from services.sequence import SequenceService

meta = MetaData()

class CustomerDAO(BaseDAO):
    def __init__(self):
        super().__init__()

        print('Initialising customer dao')

    def getRegnum(self):
        regnumLength = 6
        regnum = SequenceService().getRegnum()
        regnum = str(regnum).zfill(regnumLength)
        return regnum

    def insert(self, customer):
        now = datetime.now()
        dob = customer.get('dob')

        regnum = self.getRegnum()

        if dob == '':
            dob = None

        customer = Customers(
            regnum = regnum,
            name = customer.get('name'),
            mobile = customer.get('mobile'),
            email = customer.get('email'),
            address = customer.get('address'),
            blacklisted = customer.get('blacklisted'),
            createdat = now,
            updatedat = now,
            createdby = customer.get('createdby'),
            updatedby = customer.get('updatedby'),
            gender = customer.get('gender', 'UNKNOWN'),
            dob = dob
        )

        db.session.add(customer)
        db.session.commit()
        return 'Customer has been created successfully'

    def get(self, customerId):
        customer = Customers.query.filter_by(id=customerId).first()
        return customer

    def getByRegnum(self, regnum):
        customers = Customers.query.filter_by(regnum=regnum).all()
        return customers

    def update(self, customerId, customerObj):
        now = datetime.now()

        customer = Customers.query.get(customerId)

        customer.name = customerObj.get('name')
        customer.mobile = customerObj.get('mobile')
        customer.email = customerObj.get('email')
        customer.address = customerObj.get('address')
        customer.blacklisted = customerObj.get('blacklisted')
        customer.regnum = customerObj.get('regnum')
        customer.updatedat = now
        customer.updatedby = customerObj.get('updatedby')
        customer.gender = customerObj.get('gender')
        customer.dob = customerObj.get('dob')

        db.session.commit()
        return 'Customer has been updated successfully'

    def delete(self, customerId):
        customer = Customers.query.get(customerId)
        db.session.delete(customer)
        db.session.commit()
        return 'Customer has been deleted successfully'

    def listAll(self):
        customers = Customers.query.all()
        return customers