from flask import Flask

from services.customer import CustomerService
# from services import customer
# import importlib
# importlib.import_module('./services/customer')

app = Flask(__name__)

@app.route('/')
def hello_world():
    r = CustomerService().get(1)
    for i in r:
        print(i.name)
    # print(r.fetchall())
    # print(dir(r))
    return 'Hello, World!'
