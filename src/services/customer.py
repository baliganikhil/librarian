from services.baseService import BaseService
from daos.customer import CustomerDAO

class CustomerService(BaseService):
    def get(self, customerId):
        r = CustomerDAO().get(customerId)
        return r

    def getByRegnum(self, regnum):
        r = CustomerDAO().getByRegnum(regnum)
        return r

    def create(self, customerObj):
        return CustomerDAO().insert(customerObj)

    def update(self, customerId, customerObj):
        return CustomerDAO().update(customerId, customerObj)

    def delete(self, customerId):
        return CustomerDAO().delete(customerId)

    def listAll(self):
        return CustomerDAO().listAll()