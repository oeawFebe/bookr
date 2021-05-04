from django import template
register=template.Library()

@register.simple_tag
def generic_simple_tag(arg1,arg2):
    return ""