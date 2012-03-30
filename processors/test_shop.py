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

    class Order(object):
        def __init__(self):
            self.contact = Contact()

    c = Contact()
    c.first_name="Luther"
    c.last_name="Kurkowski"

    print "Contact: %s %s" % (c.first_name, c.last_name)

    o = Order()
    o.contact=c
    o.total=420
    #o.auth="sale"
    o.auth="store"
    #o.cycle=""
    o.cycle="3m"
    #o.payments=""
    o.payments="48"
    o.start_date="2012-05-01"
    o.avs=False
    o.bill_street = "1234 Main St."
    o.bill_city = "Springfield"
    o.bill_state = "MA"
    o.bill_postal_code = "08003"
    o.bill_country = "United States"
    o.operator = "DJ Forms"
    cc = {'billing_name':"%s %s" % (c.first_name, c.last_name), 'card_number':"4111111111111111",'expiration_month':"02",'expiration_year':"2013", 'security_code':"123"}

    exp = "%.2d%.2d" % (int(cc['expiration_month']), (int(cc['expiration_year']) % 100))
    print exp

    pp = PaymentProcessor(cc, o)
    print "status = %s" % pp.status
    print "success = %s" % pp.success
    print "msg = %s" % pp.msg

"""
status = approved
success = True
msg = {'status': 'approved', 'cvv': 'M', 'transid': '023-0108310645', 'billingid': 'N3GGRY', 'avs': '0'}
"""
