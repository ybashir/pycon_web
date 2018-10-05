import json
import logging

from django.db import models

from pycon_web.apps.mixin import CreateUpdateMixin
from pycon_web.apps.payments.api.v1.easypay_helper import EasyPayPaymentMethod, EasyPayException, \
    EasyPayAPIHelper

logger = logging.getLogger(__name__)


TRANSACTION_STATUS_INITIAL = 'initial'
TRANSACTION_STATUS_PENDING = 'pending'
TRANSACTION_STATUS_SUCCESS = 'success'
TRANSACTION_STATUS_FAILURE = 'fail'

TRANSACTION_STATUS_CHOICES = (
    (TRANSACTION_STATUS_SUCCESS, 'Transaction successful.'),
    (TRANSACTION_STATUS_PENDING, 'Transaction in progress.'),
    (TRANSACTION_STATUS_FAILURE, 'Transaction failed.'),
    (TRANSACTION_STATUS_INITIAL, 'Transaction initialized.'),
)


class PaymentMethod(CreateUpdateMixin):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    merchant_config = models.TextField()

    def __str__(self):
        return '{name}'.format(name=self.name)

    def get_value_or_none(self, key):
        try:
            configuration = json.loads(self.merchant_config)
            return configuration.get(key, None)
        except:
            logger.exception('Exception while parsing Easypay Config')
            return None


class Payment(CreateUpdateMixin):
    '''
    This is an abstract model for payments
    It contains all basic information which are possibly required in order to add a payment
    Every payment option should inherit from this model as dine for EasyPay and Jazzcash
    '''
    amount = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)

    transaction_status = models.CharField(max_length=25, choices=TRANSACTION_STATUS_CHOICES,
                                          default=TRANSACTION_STATUS_INITIAL)

    payment_method = models.ForeignKey(to=PaymentMethod)


class EasyPayPayment(Payment):
    payment_token = models.CharField(max_length=50, null=True, blank=True,
                                     help_text='EasyPay generated token in case of OTC transactions')
    transaction_id = models.CharField(max_length=50, null=True, blank=True,
                                      help_text='EasyPay generated Order ID (only for Mobile Account)')
    transaction_expiry_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{amount} - {mobile_no} - {transaction_type}'.format(amount=self.amount,
                                                                    mobile_no=self.mobile_number,
                                                                    transaction_type=self.payment_method.name)

    @classmethod
    def create(cls, transaction_amount, mobile_number, payment_method):
        payment_object = cls(amount=transaction_amount, mobile_number=mobile_number,
                             payment_method=payment_method)

        payment_object.save()
        return payment_object

    def make_payment(self, buyer_email):
        if self.transaction_status in [TRANSACTION_STATUS_SUCCESS, TRANSACTION_STATUS_FAILURE]:
            raise EasyPayException('Payment already processed for this instance')
        try:
            easy_pay_api_helper = EasyPayAPIHelper(self.payment_method)
            self.transaction_status = TRANSACTION_STATUS_INITIAL
            easy_pay_payment_method = EasyPayPaymentMethod[self.payment_method.name]
            transaction_type = easy_pay_payment_method.value
            self.payment_token, self.transaction_id, self.transaction_expiry_datetime = easy_pay_api_helper \
                .initiate_transaction(
                                    amount=self.amount,
                                    easypay_transaction_type=easy_pay_payment_method,
                                    mobile_number=self.mobile_number,
                                    email_address=buyer_email
            )
            if transaction_type == EasyPayPaymentMethod.MA.value:
                self.transaction_status = TRANSACTION_STATUS_SUCCESS
                message = 'Success making payment via EasyPay.'
            else:
                message = 'Success generating voucher via EasyPay OTC.'
                self.transaction_status = TRANSACTION_STATUS_PENDING

            success = True
        except EasyPayException as epe:
            self.transaction_status = TRANSACTION_STATUS_FAILURE
            logger.exception('Exception with EasyPay PG')
            success, message = False, str(epe)

        self.save()
        return success, message