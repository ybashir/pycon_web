from django.contrib import admin

from .models import PaymentMethod, EasyPayPayment


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']


class EasyPayPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_method']


admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(EasyPayPayment, EasyPayPaymentAdmin)
