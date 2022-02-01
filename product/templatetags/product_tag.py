from django import template
import re
import math

register = template.Library()


@register.filter
def add(value, arg):
    return value + arg


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def multiply(value, arg):
    result = float(value) * int(arg)
    return result


@register.filter
def price(value, part=True):
    value = float(value)

    if part:
        return str(math.floor(value))
    else:
        result = str(round(value, 2)).split(".")[1]
        if len(result) == 1:
            result += "0"
        return result
