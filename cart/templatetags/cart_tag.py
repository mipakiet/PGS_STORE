from django import template
import re

register = template.Library()


@register.filter
def count_cart_items(dictionary):
    result = 0
    for key, item in dictionary:
        result += item["quantity"]
    return result
