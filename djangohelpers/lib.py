from django.http import HttpResponseNotAllowed
try:
    from django.template.response import TemplateResponse
except ImportError:
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    def TemplateResponse(request, template, context=None, mimetype=None, status=None, content_type=None, current_app=None):
        return render_to_response(template, context, context_instance=RequestContext(request), mimetype=content_type or mimetype)

class rendered_with(object):
    """ use like
    @rendered_with('foo.html')
    def my_view_handler(request, ...):
      ...
    """
    def __init__(self, template_name, mimetype=None):
        self.template_name = template_name
        self.mimetype = mimetype
        
    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            if not isinstance(response, dict):
                # let inner function implicitly opt out from rendered_with
                # for explicit control of rendering, or redirects, etc
                return response
            items = response
            items.setdefault('template_name',self.template_name)
            items.setdefault('controller_name','%s/%s'%(func.__module__,func.__name__) )
            return TemplateResponse(request, self.template_name, items, mimetype=self.mimetype)
        return rendered_func

class allow_http(object):
    """ use like
    @allow_http("GET", "POST")
    def my_view_handler(request, ...):
      ...
    """

    def __init__(self, *methods):
        self.methods = methods

    def __call__(self, func):
        def inner(request, *args, **kwargs):
            if request.method not in self.methods:
                return HttpResponseNotAllowed(self.methods)
            return func(request, *args, **kwargs)
        return inner

def register_admin(model):
    from django.contrib import admin
    
    class Admin(admin.ModelAdmin):
        list_display = [f.name for f in model._meta.fields]

    admin.site.register(model, Admin)
