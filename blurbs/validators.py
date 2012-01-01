from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

def validate_wordcount(count):
    def inner(value):
        if len(strip_tags(value).split()) > count:
            raise ValidationError(u'Blurb should contain at most 250 words.')
    return inner
