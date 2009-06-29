from django import template

def chunk(chunkable, size=2):
    chunkable = list(chunkable)
    counter = 0
    chunked = []
    sublist = []
    while len(chunkable):
        for i in range(size):
            sublist.append(chunkable.pop(0))
        chunked.append(sublist)
        sublist = []
    return chunked

class TemplateTagNode(template.Node):

    noun_for = {'by': 'who'}

    @classmethod
    def error_msg(cls):
        parts = []
        for preposition, noun in cls.noun_for.items():
            parts.append("%s <%s>" % (preposition, noun))
        parts = ' '.join(parts)

        msg = """Invalid tag syntax "%s"
Syntax: %s """ + parts + """ as <varname>"""
        return msg

    @classmethod
    def process_tag(cls, parser, token):
        words = token.split_contents()
        tag_name, words = words[0], words[1:]

        _as, varname = words[-2:]
        words = words[:-2]

        if _as != 'as':
            raise template.TemplateSyntaxError, \
                cls.error_msg() % (token.contents, tag_name)
        
        words = chunk(words)
        if len(words) != len(cls.noun_for):
            raise template.TemplateSyntaxError, \
                cls.error_msg() % (token.contents, tag_name)
    
        kw = {}
        for phrase in words:
            preposition, noun = phrase
            if preposition not in cls.noun_for \
                    or cls.noun_for[preposition] in kw:
                raise template.TemplateSyntaxError, \
                    cls.error_msg() % (token.contents, tag_name)
            kw[cls.noun_for[preposition]] = noun

        return cls(varname, **kw)

    def __init__(self, varname, **kw):
        self.varname = varname
        self.vars = {}
        for key, var in kw.items():
            self.vars[key] = template.Variable(var)

    def render(self, context):
        vars = dict(self.vars)
        for key, var in vars.items():
            vars[key] = var.resolve(context)

        context[self.varname] = self.execute_query(**vars)
        return ''
    
    def execute_query(self, **kw):
        return ''
