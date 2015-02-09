DECLINE_CODES = {
    "decline" : "The credit card was declined",
    "avs" : "AVS failed; the address entered does not match the billing address on file at the bank",
    "cvv" : "CVV failed; the number provided is not the correct verification number for the card",
    "call" : "The card must be authorized manually over the phone",
    "expiredcard" : "Issuer was not certified for card verification",
    "carderror" : "Card number is invalid",
    "authexpired" : "Attempt to postauth an expired (more than 14 days old) preauth",
    "fraud" : "CrediGuard fraud score was below requested threshold",
    "blacklist" : "CrediGuard blacklist value was triggered",
    "velocity" : "CrediGuard velocity control value was triggered",
    "dailylimit" : "Daily limit in transaction count or amount as been reached",
    "weeklylimit" : "Weekly limit in transaction count or amount as been reached",
    "monthlylimit" : "Monthly limit in transaction count or amount as been reached"
}
BADDATA_CODES = {
    "missingfields" : "One or more parameters required for this transaction type were not sent",
    "extrafields" : "Parameters not allowed for this transaction type were sent",
    "badformat" : "A field was improperly formatted, such as non-digit characters in a number field",
    "badlength" : "A field was longer or shorter than the server allows",
    "merchantcantaccept" : "The merchant can't accept data passed in this field",
    "mismatch" : "Data in one of the offending fields did not cross-check with the other offending field"
}
ERROR_CODES = {
    "cantconnect" : "Couldn't connect to the TrustCommerce gateway",
    "dnsfailure" : "The TCLink software was unable to resolve DNS hostnames",
    "linkfailure" : "The connection was established, but was severed before the transaction could complete",
    "failtoprocess" : "The bank servers are offline and unable to authorize transactions"
}
