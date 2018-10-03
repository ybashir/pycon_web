from django.conf.urls import url

from theme import views


urlpatterns = [
    url(r'^speakers/(?P<year>[0-9]{4})/$', views.SpeakersIndexView.as_view(), name='speakers_index'),
    url(r'^gallery/$', views.GalleryIndexView.as_view(), name='gallery_index'),
    url(r'^gallery/(?P<slug>[\w-]+)/$', views.GalleryDetailView.as_view(), name='gallery_detail'),
]
