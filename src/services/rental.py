from datetime import datetime, timedelta

from services.baseService import BaseService
from daos.rental import RentalDAO, RentalStatus

from services.book import BookService
from services.bookunit import BookunitService
from services.customer import CustomerService

class RentalService(BaseService):
    def processCartForDisplay(self, cart):
        totalCharge = 0
        for cartItem in cart:
            totalCharge = totalCharge + cartItem.get('charge', 0)
            cartItem['duedate'] = datetime.strptime(cartItem.get('duedate'), '%Y-%m-%d %H:%M:%S')

        return cart, totalCharge

    def get(self, rentalId):
        r = RentalDAO().get(rentalId)
        return r

    def addToRentalCart(self, customerId, bookBarcode, cart):
        bookunit = BookunitService().getByBarcode(bookBarcode)

        # Check if the incoming book unit is a valid book
        if bookunit == None:
            raise Exception('Invalid barcode - No such book found')

        bookunitId = bookunit.id
        bookId = bookunit.bookId

        # Check if the book unit has already been added
        for cartItem in cart:
            if cartItem.get('bookunitId') == bookunitId:
                raise Exception('Duplicate barcode - This book was already scanned')

        # Throw an error if book was already rented
        rentalObj = RentalDAO().getRentalForReturn(bookunitId)
        if rentalObj != None:
            raise Exception('Invalid barcode - This book is already rented')

        book = BookService().get(bookId)
        rentduration = book.rentduration
        charge = book.charge

        now = datetime.now()
        duedate = now + timedelta(days=rentduration)

        rentalObj = {
            'bookunitId': bookunitId,
            'customerId': customerId,
            'duedate': duedate.strftime('%Y-%m-%d %H:%M:%S'),
            'status': RentalStatus.get('RENTED'),
            'comments': '',
            'charge': charge,
            'bookId': bookId,
            'title': book.title
        }

        cart.append(rentalObj)

        return cart

    def addToReturnCart(self, bookBarcode, cart):
        bookunit = BookunitService().getByBarcode(bookBarcode)

        # Check if the incoming book unit is a valid book
        if bookunit == None:
            raise Exception('Invalid barcode - No such book found')

        # Check if the book unit has already been added
        for cartItem in cart:
            if cartItem.get('bookunitId') == bookunit.id:
                raise Exception('Duplicate barcode - This book was already scanned')

        bookunitId = bookunit.id

        rentalObj = RentalDAO().getRentalForReturn(bookunitId)

        # Throw an error if a valid rental was not found
        if rentalObj == None:
            raise Exception('Invalid barcode - No active rental found')

        book = BookService().get(bookunit.bookId)

        curCartItem = rentalObj.to_dict()
        curCartItem['title'] = book.title
        cart.append(curCartItem)

        return cart

    def returnRentals(self, cart):
        rentalIds = []
        for cartItem in cart:
            rentalIds.append(cartItem.get('id'))

        return RentalDAO().markReturned(rentalIds), 'Rentals were marked as returned'

    def create(self, cart):
        cartSize = len(cart)
        i = 1

        for cartItem in cart:
            commit = i == cartSize
            i = i + 1
            print('Adding item ' + str(commit))
            RentalDAO().insert(cartItem, commit)

    def update(self, rentalId, rentalObj):
        return RentalDAO().update(rentalId, rentalObj)

    def delete(self, rentalId):
        return RentalDAO().delete(rentalId)

    def listActiveForCustomer(self, customerId):
        activeRentals = RentalDAO().listActiveForCustomer(customerId)

        for activeRental in activeRentals:
            bookunitId = activeRental.bookunitId
            book = BookunitService().getBookByBookunitId(bookunitId)
            activeRental.title = book.title

        return activeRentals

    def listHistoryForCustomer(self, customerId):
        historicRentals = RentalDAO().listHistoryForCustomer(customerId)

        for historicRental in historicRentals:
            bookunitId = historicRental.bookunitId
            book = BookunitService().getBookByBookunitId(bookunitId)
            historicRental.title = book.title

        return historicRentals

    def listAllActive(self):
        activeRentals = RentalDAO().listAllActive()

        for activeRental in activeRentals:
            bookunitId = activeRental.bookunitId
            customerId = activeRental.customerId
            book = BookunitService().getBookByBookunitId(bookunitId)
            customer = CustomerService().get(customerId)

            activeRental.title = book.title
            activeRental.customerName = customer.name

        return activeRentals