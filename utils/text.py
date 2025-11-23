from unidecode import unidecode
from django.utils.text import slugify


def slugify_unidecode(text):
    return slugify(unidecode(title))
