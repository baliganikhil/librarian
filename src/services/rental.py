from datetime import datetime, timedelta

from services.baseService import BaseService
from daos.rental import RentalDAO, RentalStatus

from services.book import BookService
from services.bookunit import BookunitService

class RentalService(BaseService):
    def getTotalCharge(self, cart):
        totalCharge = 0
        for cartItem in cart:
            totalCharge = totalCharge + cartItem.get('charge', 0)

        return totalCharge

    def get(self, rentalId):
        r = RentalDAO().get(rentalId)
        return r

    def addToCart(self, customerId, bookBarcode, cart):
        bookunit = BookunitService().getByBarcode(bookBarcode)
        bookunitId = bookunit.id
        bookId = bookunit.bookId

        book = BookService().get(bookId)
        rentduration = book.rentduration
        charge = book.charge

        now = datetime.now()
        # today = datetime.strptime(now, "%d/%m/%y")
        duedate = now + timedelta(days=rentduration)

        rentalObj = {
            'bookunitId': bookunitId,
            'customerId': customerId,
            'duedate': duedate,
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

        if bookunit == None:
            raise Exception('Invalid barcode - No such book found')

        bookunitId = bookunit.id

        rentalObj = RentalDAO().getRentalForReturn(bookunitId)
        book = BookService().get(bookunit.bookId)

        curCartItem = rentalObj.to_dict()
        curCartItem['title'] = book.title
        cart.append(curCartItem)

        for cartItem in cart:
            cartItem['duedate'] = datetime.strptime(cartItem.get('duedate'), '%Y-%m-%d %H:%M:%S')

        return cart

    def returnRentals(self, cart):
        rentalIds = []
        for cartItem in cart:
            rentalIds.append(cartItem.get('id'))

        return RentalDAO().markReturned(rentalIds)


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