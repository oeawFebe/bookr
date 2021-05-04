from django import template
register=template.Library()
@register.simple_tag(takes_context=True)
def contextual_greet_user(context,message):
    username=context['username']
    return f"{message}, {username}!!!"