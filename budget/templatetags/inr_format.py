from django import template
from django.conf import settings
import locale

register = template.Library()
locale.setlocale(locale.LC_ALL, settings.LC_FORMAT)


@register.filter(name='INR')
def inr(value):
    try:
        value = float(value)
        return locale.currency(value, grouping=True)
    except (ValueError, TypeError):
        return value