from django.conf.urls import url

from pycon_web.apps.payments.api.v1.views import MakePayment

urlpatterns = [
    url(r'^make_payment/?$', MakePayment.as_view(), name='make_payment')
]