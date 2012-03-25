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
        self.cycle = settings.TC_CYCLE
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

        # auth type
        action = self.auth
        if data.auth == "subscription":
            action = "store"

        # override avs from form
        if data.avs == 'y':
            self.avs = 'y'

        # billing period
        if data.cycle:
            self.cycle = data.cycle

        self.transactionData = {
            # account data
            'custid'        : self.custid,
            'password'      : self.password,
            'demo'          : self.demo,
            # customer data
            'name'          : data.contact.first_name + u' ' + data.contact.last_name,
            # transaction data
            'media'         : 'cc',
            'action'        : action,
            'amount'        : amount,           # in cents
            'cc'            : data.card.num,    # use '4111111111111111' for test
            'exp'           : exp,              # 4 digits eg 0108
            'cvv'           : data.card.ccv,
            'avs'           : self.avs          # address verification - see tclink dev guide
        }

        # address verification
        if avs == 'y':
            self.transactionData['address1'] = data.bill_street1
            self.transactionData['city']     = data.bill_city
            self.transactionData['state']    = data.bill_state
            self.transactionData['zip']      = data.bill_postal_code
            self.transactionData['country']  = data.bill_country

        # subscription/recurring billing
        if action == "subscription":
            self.transactionData['cycle'] = self.cycle
            self.transactionData['payments'] = data.payments

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
            if status == 'declined':
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
