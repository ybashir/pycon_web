from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from pycon_web.apps.payments.api.v1.serializers import MakePaymentRequestSerializer
from pycon_web.apps.payments.api.v1.utils import attempt_transaction, failure_response
from pycon_web.apps.payments.models import EasyPayPayment


class MakePayment(APIView):

    def post(self, request):
        try:
            request_serializer = MakePaymentRequestSerializer(data=request.data)
            request_serializer.is_valid(raise_exception=True)
            request_data = request_serializer.validated_data

            payment_method = request_data['payment_method']
            mobile_number = request_data['mobile_number']
            if not mobile_number:
                raise Exception("Mobile number not found.")

            transaction_amount = request_data['transaction_amount']
            email = request_data.get('email', "pycon_arbisoft@gmail.com")

            if payment_method.code in ['EASYPAY_MA', 'EASYPAY_OTC']:
                payment = EasyPayPayment.create(transaction_amount, mobile_number,
                                                payment_method)

                response = attempt_transaction(payment, email)

                return response

        except ValidationError as ve:
            return failure_response(failure_message=ve, status_code=400)
