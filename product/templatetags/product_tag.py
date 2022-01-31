from django import template
import re

register = template.Library()


@register.filter
def add(value, arg):
    return value + arg


@register.filter
def sub(value, arg):
    return value - arg
