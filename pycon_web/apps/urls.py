from django.conf.urls import url, include

from pycon_web.apps.payments.urls import urlpatterns as payment_urls

v1_url_regex_pattern = r'^v1/'

urlpatterns = [
    url(v1_url_regex_pattern, include(payment_urls))
]
