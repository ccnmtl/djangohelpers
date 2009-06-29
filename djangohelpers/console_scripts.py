"""
Generates a new template tag and writes it to stdout.

Usage:
maketemplatetag template_tag_name callableToExecute a=b c=d e=f

e.g.
`maketemplatetag get_relevant_foos getFoos for=user in=location`
will generate a template tag that can be used like:
{% get_relevant_foos for user in location %}

defining `getFoos` is up to you; after the code has been generated
you'll see what you need to do much more easily than I can explain
in documentation.
"""

def subclass_templatetag(tag_name, query, query_args=None):
    classname = ''.join(i.title() for i in tag_name.split('_'))
    prep_dict = "{" + ', '.join('"%s":"%s"' % tuple(arg.split('=')) for arg in query_args) + "}"
    query_args = [arg.split('=')[1] for arg in query_args]
    init_args = ', '.join(query_args)

    unfolded_dict = ', '.join('%s=%s' % (arg,arg) for arg in query_args)

    subclass = """
from django import template

from djangohelpers.templatetags import TemplateTagNode

class %(classname)s(TemplateTagNode):

    noun_for = %(prep_dict)s

    def __init__(self, varname, %(init_args)s):
        TemplateTagNode.__init__(self, varname, %(unfolded_dict)s)

    def execute_query(self, %(init_args)s):
        return %(query)s(%(unfolded_dict)s)

register = template.Library()
register.tag('%(tag_name)s', %(classname)s.process_tag)
"""
    return subclass % locals()

def main():
    import sys
    sys.argv = sys.argv[1:]
    try:
        print subclass_templatetag(sys.argv[0], sys.argv[1], sys.argv[2:])
    except:
        print __doc__

if __name__ == '__main__':
    main()
