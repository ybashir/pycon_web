import os

from django.core.management.base import BaseCommand

from theme.models import Gallery, GalleryImage


class Command(BaseCommand):
    help = 'adds images to the gallery'

    def add_arguments(self, parser):
        parser.add_argument('slug', type=str, help='url slug of the gallery to be populated')
        parser.add_argument('dir', type=str, help='path to directory where images are')

    def handle(self, *args, **kwargs):
        slug = kwargs['slug']
        dir_name = kwargs['dir']

        gallery = Gallery.objects.filter(slug=slug).first()
        for img in [os.path.join(dir_name, file) for file in os.listdir(dir_name)]:
            GalleryImage.objects.create(gallery=gallery, image=img[13:])
