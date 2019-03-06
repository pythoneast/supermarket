from django import template
register = template.Library()


@register.simple_tag
def upper_string(value):
    return value.upper()


@register.filter
def lower_string(value):
    return value.lower()