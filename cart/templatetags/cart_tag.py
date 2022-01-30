from django import template
import re

register = template.Library()


@register.filter
def multiply(value, arg):
    result = str(round((float(value) * arg), 2))
    if re.search("\.[0-9]$", result):
        result += "0"
    return result


@register.filter
def count_cart_items(dictionary):
    result = 0
    for key, item in dictionary:
        result += item["quantity"]
    return result
