from services.baseService import BaseService
from daos.customer import CustomerDAO

class CustomerService(BaseService):
    def get(self, customerId):
        return CustomerDAO().get(customerId)
        # pass