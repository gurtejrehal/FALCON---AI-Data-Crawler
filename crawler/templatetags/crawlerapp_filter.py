from django import template

register = template.Library()

@register.filter(name='change_string')
def change_string(value):
    return value.replace('_', ' ').title()


# register.filter('string_format', string_format)
