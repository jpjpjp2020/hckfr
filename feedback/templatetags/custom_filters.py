"""
In overisght db and nested logic - to use journey clarity and reduce unnecessesay discovery
"""

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)