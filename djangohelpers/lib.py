from django.http import HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext

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
            if self.mimetype is not None:
                return render_to_response(self.template_name, items, 
                                          context_instance=RequestContext(request),
                                          mimetype=self.mimetype)
            else:
                return render_to_response(self.template_name, items, 
                                          context_instance=RequestContext(request))

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

