from rest_framework import serializers

from pycon_web.apps.payments.models import PaymentMethod


class MakePaymentRequestSerializer(serializers.Serializer):
    payment_method = serializers.SlugRelatedField(slug_field='code',
                                                  queryset=PaymentMethod.objects.all())
    mobile_number = serializers.CharField(required=True)
    transaction_amount = serializers.IntegerField(required=True)
    email = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_mobile_number(self, mobile_number):
        if len(mobile_number) != 11:
            raise serializers.ValidationError("Invalid Mobile Number")

        return mobile_number
