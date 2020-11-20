from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime, Date, Text
from flask_sqlalchemy import SQLAlchemy

from main import db
from daos.basedao import BaseDAO
from models.customer import Customers

meta = MetaData()

class CustomerDAO(BaseDAO):
    def __init__(self):
        super().__init__()

        print('Initialising customer dao')

    def insert(self, customer):
        now = datetime.now()

        customer = Customers(
            name = customer.get('name'),
            mobile = customer.get('mobile'),
            email = customer.get('email'),
            address = customer.get('address'),
            blacklisted = customer.get('blacklisted'),
            regnum = customer.get('regnum'),
            createdat = now,
            updatedat = now,
            createdby = customer.get('createdby'),
            updatedby = customer.get('updatedby'),
            gender = customer.get('gender', 'UNKNOWN'),
            dob = customer.get('dob')
        )

        db.session.add(customer)
        db.session.commit()
        return 'Customer has been created successfully'

    def get(self, customerId):
        customer = Customers.query.filter_by(id=customerId).first()
        return customer

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