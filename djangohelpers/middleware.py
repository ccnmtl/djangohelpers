from django.shortcuts import render_to_response

class HttpDeleteMiddleware(object):
    def process_request(self, request):
        if not request.GET.has_key('delete'):
            return None
        if request.method == "GET":
            return render_to_response('djangohelpers/confirm_delete.html')
        if request.method == "POST":
            request.method = "DELETE"

def path_matches(current_path, paths_to_match):
    for exempt_path in paths_to_match:
        try:
            if current_path.startswith(exempt_path):
                return True
        except TypeError: # it wasn't a string object .. must be a regex
            if exempt_path.match(current_path):
                return True

    return False

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.http import urlquote
from django.http import HttpResponseRedirect
class AuthRequirementMiddleware(object):
    def process_request(self, request):
        path = urlquote(request.get_full_path())           

        if path_matches(path, getattr(settings, 'ANONYMOUS_PATHS', [])):
            return None

        if request.user.is_authenticated():
            return None

        return HttpResponseRedirect('%s?%s=%s' % (
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
                path))

from django.http import HttpResponseForbidden

class GroupRequirementMiddleware(object):
    def process_request(self, request):
        path = urlquote(request.get_full_path())

        permission_locks = getattr(settings, 'GROUP_REQUIREMENTS_PER_PATH', {})
        first_match = path_matches(path, permission_locks.keys())

        if not first_match:
            return None

        required_permission = permission_locks[first_match]
        from django.contrib.auth.models import Group

        required_permission = Group.objects.get(name=required_permission)

        if required_permission in request.user.groups.all():
            return None

        if request.user.is_anonymous():
            return HttpResponseRedirect('%s?%s=%s' % (
                    settings.LOGIN_URL,
                    REDIRECT_FIELD_NAME,
                    path))


        location = getattr(settings, 'GROUP_REQUIREMENTS_REDIRECT', None)
        if location:
            return HttpResponseRedirect(location)

        return HttpResponseForbidden("Insufficient priviledges")
        
