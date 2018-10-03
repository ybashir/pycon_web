from django.views import generic
from theme.models import Gallery


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
