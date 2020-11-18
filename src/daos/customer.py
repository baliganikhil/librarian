from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, DateTime, Date, Text
from daos.basedao import BaseDAO

meta = MetaData()

class CustomerDAO(BaseDAO):
    customersTable = Table(
            'customers', meta,
            Column('id', Integer, primary_key = True),
            Column('name', String),
            Column('mobile', String),
            Column('email', String),
            Column('address', Text),
            Column('blacklisted', Boolean),
            Column('regnum', String),
            Column('createdat', DateTime),
            Column('updatedat', DateTime),
            Column('createdby', String),
            Column('updatedby', String),
            Column('gender', String),
            Column('dob', Date)
        )

    def __init__(self):
        super().__init__()

        print('Initialising customer dao')

        # self.customersTable =

    def insert(self, customer):
        pass

    def get(self, customerId):
        s = self.customersTable.select()
        return self.conn.execute(s)

    def update(self, customer):
        pass

    def delete(self, customerId):
        pass