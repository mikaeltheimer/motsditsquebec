from django import template
register = template.Library()


@register.filter(name='ng')
def angularjs(string):
    '''Render as an angularjs template tag'''
    return "{{" + string + "}}"
