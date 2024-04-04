
from django import template
from ..services import get_place_photos

register = template.Library()


@register.filter
def make_photo_url(photo_reference):
    return get_place_photos(photo_reference)
