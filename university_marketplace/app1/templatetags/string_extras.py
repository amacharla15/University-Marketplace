# app1/templatetags/string_extras.py
from django import template
register = template.Library()

@register.filter
def repeat(char, times):
    return char * times
