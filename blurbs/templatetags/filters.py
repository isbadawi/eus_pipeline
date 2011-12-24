from django import template

register = template.Library()

@register.filter
def numberify(n):
    return '%02d.' % n             
