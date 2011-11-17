from django import template
from djangohelpers.templatetags import TemplateTagNode

register = template.Library()

class ReplaceValue(TemplateTagNode):
    """
    Copies a dict with a value swapped; for example:
      >> my_dict = {'a': 1, 'b': 2, 'c': 3}
      >> {% replace_value of 'b' with 7 in my_dict as new_dict %}
      >> new_dict
      {'a': 1, 'b': 7, 'c': 3}

    Set a value to the empty string to silently delete it:
      >> {% replace_value of 'b' with '' in my_dict as new_dict %}
      >> new_dict
      {'a': 1, 'c': 3}
    """
    noun_for = {"of":"key", "in":"items", "with":"value"}

    def __init__(self, varname, key, items, value):
        TemplateTagNode.__init__(self, varname, key=key, items=items, value=value)

    def execute_query(self, key, items, value):
        new = dict(items)
        if value == '':
            del new[key]
        else:
            new[key] = value
        return new
register.tag('replace_value', ReplaceValue.process_tag)

def qsify(_dict):
    """
    converts a dict into a query string:
     {{my_dict|qsify}}
    """
    qs = '?'
    try:
        iterator = _dict.iterlists()
    except AttributeError:
        iterator = _dict.iteritems()

    for key, value in iterator:
        if isinstance(value, list):
            for v in value:
                qs += '%s=%s&' % (key, v)
        else:
            qs += '%s=%s&' % (key, value)
    qs=qs.rstrip("&")
    return qs
register.filter('qsify', qsify)

def split(text):
    """ sometext|split """
    return text.split()
register.filter('split', split)

def getitem(dict, item):
    """ my_dict|getitem:'b' """
    try:
        return dict[item]
    except KeyError:
        return ''
register.filter('getitem', getitem)

def lessthan(a, b):
    return a < b
register.filter('lessthan', lessthan)

def greaterthan(a, b):
    return a > b
register.filter('greaterthan', greaterthan)
