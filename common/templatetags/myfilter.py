from django import template
import re

register = template.Library()

@register.filter
def spacify(value):
    spac = '&'+'nbsp;'
    esc = lambda x: x
    tabSpac = re.sub('\t', spac*4, esc(value))
    return tabSpac

@register.filter
def myspace(value):
    spac = '&'+'nbsp;'
    myspac = value.replace(' ', spac)
    return myspac