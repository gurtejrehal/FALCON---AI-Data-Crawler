from django import template
import json

register = template.Library()

@register.filter(name='change_string')
def change_string(value):
    return value.replace('_', ' ').title()


@register.filter(name='format_id')
def format_id(value):
    return value.replace(' ', '-').title()

@register.filter(name='count_items')
def count_items(value):
    return value.count()

@register.filter(name='jsonify_data')
def jsonify_data(value):
    print(json.dumps(value))
    return json.dumps(value)

# register.filter('string_format', string_format)
