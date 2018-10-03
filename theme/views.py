from django.views import generic
from theme.models import Gallery, Speaker


class SpeakersIndexView(generic.ListView):
    template_name = 'pages/speakers.html'
    context_object_name = 'speakers'

    def get_queryset(self):
        return Speaker.objects.published().filter(conference_year=self.kwargs['year'])


class GalleryIndexView(generic.ListView):
    template_name = 'gallery/index.html'
    context_object_name = 'galleries'

    def get_queryset(self):
        return Gallery.objects.published()


class GalleryDetailView(generic.DetailView):
    template_name = 'gallery/detail.html'
    context_object_name = 'gallery'

    def get_queryset(self):
        return Gallery.objects.published()
