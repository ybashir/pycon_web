from django.conf.urls import url, include

from pycon_web.apps.payments.api.v1.urls import urlpatterns as v1

urlpatterns = [
    url(r'^pycon_payments/', include(v1)),
]
