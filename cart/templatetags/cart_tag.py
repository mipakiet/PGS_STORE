from django import template

register = template.Library()


@register.filter()
def multiply(value, arg):
    result = str(float(value) * arg)
    if ".0" in result:
        return result + "0"
    return result
