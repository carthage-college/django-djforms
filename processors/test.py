from django.conf import settings
from djforms.processors.trust_commerce import PaymentProcessor

from decimal import Decimal

if __name__ == "__main__":
    #####
    # test a processor
    #####

    # dummy classes to hold data
    class Contact(object):
        pass

    class Card(object):
        pass

    class Order(object):
        def __init__(self):
            self.contact = Contact()
            self.card = Card()

    c = Contact()
    c.first_name="Luther"
    c.last_name="Kurkowski"

    print "Contact: %s %s" % (c.first_name, c.last_name)

    o = Order()
    o.contact=c
    o.total=420
    o.bill_street1 = "1234 Main St."
    o.bill_street2 = "Suite 16"
    o.bill_city = "Springfield"
    o.bill_state = "MA"
    o.bill_postal_code = "08003"
    o.bill_country = "United States"
    cc = Card()
    cc.num = "4111111111111111"
    #cc.num = "1234123412341234"
    cc.expire_month = "02"
    cc.expire_year = "2013"
    cc.ccv = "123"
    o.card = cc
    o.operator = "DJ Forms"

    print o.card.num
    print o.card.ccv
    print o.operator
    exp = "%.2d%.2d" % (int(o.card.expire_month), (int(o.card.expire_year) % 100))
    print exp

    pp = PaymentProcessor(o)
    print "status = %s" % pp.status
    print "success = %s" % pp.success
    print "msg = %s" % pp.msg

