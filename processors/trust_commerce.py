from django.conf import settings

import tclink

class PaymentProcessor():
    """
    TrustCommerce payment processing module.
    Reqs:
    1) order object
    2) contact object within order object
    3) card object within order object
    """

    def __init__(self, order=None):
        self.demo = 'y'
        self.AVS = 'n'
        self.custid = settings.TC_LOGIN
        self.password = settings.TC_PASSWORD
        if not settings.TC_LIVE:
            self.demo = 'n'
        if settings.TC_AVS:
            self.AVS = 'y'
        self.auth = settings.TC_AUTH_TYPE
        self.tclink_version = tclink.getVersion()
        self.order = order
        self.status = None
        self.success = None
        self.msg = None
        self.response = self.capture_payment()

    def prepare_post(self, data):
        # See tclink developer's guide for additional fields and info.
        # Convert amount to cents, no decimal point
        amount = unicode((data.total * 100))

        # convert exp date to mmyy from mm/yy or mm/yyyy
        exp = u"%.2d%.2d" % (int(data.card.expire_month), (int(data.card.expire_year) % 100))

        self.transactionData = {
            # account data
            'custid'    : self.custid,
            'password'    : self.password,
            'demo'    : self.demo,

            # Customer data
            'name'      : data.contact.first_name + u' ' + data.contact.last_name,
            'address1'    : data.bill_street1,
            'city'    : data.bill_city,
            'state'     : data.bill_state,
            'zip'     :data.bill_postal_code,
            'country'    : data.bill_country,

            # transaction data
            'media'     : 'cc',
            'action'    : self.auth,
            'amount'     : amount,    # in cents
            'cc'    : data.card.num,  # use '4111111111111111' for test
            'exp'    : exp,         # 4 digits eg 0108
            'cvv'    : data.card.ccv,
            'avs'    : self.AVS,        # address verification - see tclink dev guide
            'operator'    : data.operator
            }
        for key, value in self.transactionData.items():
            if isinstance(value, unicode):
                self.transactionData[key] = value.encode('utf7',"ignore")

    def capture_payment(self):
        """
        process the transaction through tclink
        """

        self.prepare_post(self.order)

        result = tclink.send(self.transactionData)
        status = result ['status']
        success = False

        if status == 'approved':
            success = True
            msg = result
        else:
            if status == 'decline':
                msg = 'Transaction was declined.  Reason: %s' % result['declinetype']

            elif status == 'baddata':
                msg = 'Improperly formatted data. Offending fields: %s' % result['offenders']

            else:
                status = "error"
                msg = 'An error occurred: %s' % result['errortype']

        self.status = status
        self.success = success
        self.msg = msg

        return self
