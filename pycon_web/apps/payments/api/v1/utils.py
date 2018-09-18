import logging

from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


DEFAULT_SUCCESS_MESSAGE = 'Operation successful.'
DEFAULT_FAILURE_MESSAGE = 'Something went wrong.'


def attempt_transaction(payment, email):
    transaction_error_message = "Error while attempting transaction"
    try:
        logger.info('Attempting transactions')
        success, message = payment.make_payment(email)

    except Exception as e:
        logger.error(str(e))

        response = failure_response(failure_message=transaction_error_message,
                                    data=get_payment_messages(payment))
        return response

    if success:

        response = success_response(
            {'payment_method': get_payment_messages(payment)}, message
        )
    else:
        response = failure_response(
            failure_message=message,
            data=get_payment_messages(payment)
        )

    return response


def success_response(data=None, success_message=DEFAULT_SUCCESS_MESSAGE,
                     status_code=status.HTTP_200_OK):

    response_data = {
        'success': True,
        'message': success_message,
        'data': data
    }
    return Response(response_data, status=status_code)


def failure_response(failure_message=DEFAULT_FAILURE_MESSAGE,
                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=None):
    response_data = {
        'status_code': status_code,
        'success': False,
        'message': failure_message,
        'data': data
    }
    return Response(response_data, status=status_code)


def get_payment_messages(attrs):
    payment_method = attrs.payment_method

    if payment_method.code == 'EASYPAY_MA':
        payment_method_message = "Easypaisa mobile account"
    elif payment_method.code == 'EASYPAY_OTC':
        payment_method_message = "Easypaisa shop"
    else:
        payment_method_message = str(attrs.payment_method.code)

    return payment_method_message