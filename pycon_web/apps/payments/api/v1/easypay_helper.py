import logging
from enum import Enum

import zeep
from requests import Session
from zeep.transports import Transport


logger = logging.getLogger(__name__)


class EasyPayException(Exception):
    def __init__(self, message):
        super(EasyPayException, self).__init__(message)


class EasyPayIPNTransactionStatus(Enum):
    SUCCESSFUL = 'PAID'
    PENDING = 'PENDING'
    FAILED = 'FAILED'
    EXPIRED = 'EXPIRED'

    def is_successful(self):
        return self == EasyPayIPNTransactionStatus.SUCCESSFUL

    def easypay_payment_status(self):
        from pycon_web.apps.payments.models import TRANSACTION_STATUS_SUCCESS, TRANSACTION_STATUS_FAILURE, \
            TRANSACTION_STATUS_PENDING
        if self == EasyPayIPNTransactionStatus.SUCCESSFUL:
            return TRANSACTION_STATUS_SUCCESS
        elif self == EasyPayIPNTransactionStatus.PENDING:
            return TRANSACTION_STATUS_PENDING
        elif self == EasyPayIPNTransactionStatus.FAILED:
            return TRANSACTION_STATUS_FAILURE
        elif self == EasyPayIPNTransactionStatus.EXPIRED:
            return TRANSACTION_STATUS_FAILURE


def easypay_default_wsdl_client(wsdl_url):
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = zeep.Client(wsdl=wsdl_url, transport=transport, strict=False)
    return client


class EasyPayAPIHelper:
    def __init__(self, easypay_payment_method):
        wsdl_url = easypay_payment_method.get_value_or_none('WSDL_URL')

        self.username = easypay_payment_method.get_value_or_none('MERCHANT_USERNAME')
        self.password = easypay_payment_method.get_value_or_none('MERCHANT_PASSWORD')
        self.storeId = easypay_payment_method.get_value_or_none('STORE_ID')
        self.binding_name = easypay_payment_method.get_value_or_none('SOAP_BINDING_NAME')
        self.soap_endpoint = easypay_payment_method.get_value_or_none('SOAP_ENDPOINT')

        self.transaction_id = None
        self.transaction_datetime = None
        self.transaction_expiry_datetime = None
        self.easy_pay_voucher_code = None

        self.client = easypay_default_wsdl_client(wsdl_url)

    def initiate_transaction(self, amount, easypay_transaction_type, mobile_number, email_address=None):
        initiateTransactionHackService = self.client.create_service(self.binding_name, self.soap_endpoint)

        order_id = "Pycon-212" # setting it as constant because order functionality is missing
        params_dict = {
            'username': self.username,
            'password': self.password,
            'orderId': order_id,
            'storeId': self.storeId,
            'transactionAmount': str(amount),
            'transactionType': easypay_transaction_type.api_representation(),
            'msisdn': mobile_number,
            'mobileAccountNo': mobile_number,
            'emailAddress': email_address
        }

        logger.info('Sending request to EasyPay. Params: {}'.format(params_dict))

        result = initiateTransactionHackService.initiateTransaction(**params_dict)

        """
        Sample Response
        <?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
           <soapenv:Body>
              <ns3:initiateTransactionResponseType xmlns:ns3="http://dto.transaction.partner.pg.systems.com/" xmlns:ns2="http://dto.common.pg.systems.com/">
                 <ns2:responseCode>0000</ns2:responseCode>
                 <orderId>Pycon-2</orderId>
                 <storeId>2824</storeId>
                 <paymentToken>592342</paymentToken>
                 <transactionDateTime>2017-08-18T15:47:25.937+05:00</transactionDateTime>
                 <paymentTokenExiryDateTime>2017-08-23T15:47:25.922+05:00</paymentTokenExiryDateTime>
              </ns3:initiateTransactionResponseType>
           </soapenv:Body>
        </soapenv:Envelope>
        """

        logger.info('Response from EasyPay : {}'.format(str(result)))

        self.easy_pay_voucher_code = result['paymentToken']
        self.transaction_id = result['transactionId']
        self.transaction_datetime = result['transactionDateTime']
        self.transaction_expiry_datetime = result['paymentTokenExiryDateTime']

        status_code = EasyPayStatusCode(result['responseCode'])

        if status_code.is_successful():
            return self.easy_pay_voucher_code, self.transaction_id, self.transaction_expiry_datetime

        logger.error(result['responseCode'])
        raise EasyPayException(status_code.user_facing_message())


class EasyPayStatusCode(Enum):
    PAYMENT_SUCCESSFUL = '0000'
    SYSTEM_ERROR = '0001'
    REQUIRED_FIELD_MISSING = '0002'
    INVALID_ORDER_ID = '0003'
    MERCHANT_DOES_NOT_EXIST = '0004'
    MERCHANT_NOT_ACTIVE = '0005'
    STORE_DOES_NOT_EXIST = '0006'
    STORE_INACTIVE = '0007'

    def user_facing_message(self):
        if self == EasyPayStatusCode.PAYMENT_SUCCESSFUL:
            return 'Payment Successful.'
        elif self == EasyPayStatusCode.SYSTEM_ERROR:
            return 'System Error.'
        elif self == EasyPayStatusCode.REQUIRED_FIELD_MISSING:
            return 'A required field is missing in the request.Please make sure your ' \
                   'mobile number is correct'
        elif self == EasyPayStatusCode.INVALID_ORDER_ID:
            return 'Invalid Order ID.'
        elif self == EasyPayStatusCode.MERCHANT_DOES_NOT_EXIST:
            return 'Merchant does not exist.'
        elif self == EasyPayStatusCode.MERCHANT_NOT_ACTIVE:
            return 'Merchant not active.'
        elif self == EasyPayStatusCode.STORE_DOES_NOT_EXIST:
            return 'Store does not exist.'
        elif self == EasyPayStatusCode.STORE_INACTIVE:
            return 'Store Inactive.'

    def is_successful(self):
        return self == EasyPayStatusCode.PAYMENT_SUCCESSFUL


class EasyPayPaymentMethod(Enum):
    OTC = 0
    MA = 1

    def api_representation(self):
        if self == EasyPayPaymentMethod.OTC:
            return 'OTC'
        elif self == EasyPayPaymentMethod.MA:
            return 'MA'

    def label(self):
        if self == EasyPayPaymentMethod.OTC:
            return 'Over the Counter'
        elif self == EasyPayPaymentMethod.MA:
            return 'Mobile Account'

    def api_success_code(self):
        return EasyPayStatusCode.PAYMENT_SUCCESSFUL
