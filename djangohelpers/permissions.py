from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

class LazyPermissions(object):
    def __init__(self, request):
        self.request = request
        self._groups = None

    def __getattr__(self, permission):
        if self.request.user.is_superuser:
            return True
        if self._groups is None:
            self._groups = list(self.request.user.groups.values_list("name", flat=True))
        return permission in self._groups

def authorize(permissions):
    if isinstance(permissions, basestring):
        permissions = [permissions]
    def wrapper(func):
        def inner(request, *args, **kw):
            for permission in permissions:
                if not getattr(request.PERMISSIONS, permission):
                    return HttpResponseForbidden()
            return func(request, *args, **kw)
        return inner
    return wrapper
