from urllib.parse import quote
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render
from djangohelpers.permissions import LazyPermissions
from django.utils.deprecation import MiddlewareMixin


class HttpDeleteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'delete' not in request.GET:
            return None
        if request.method == "GET":
            return render(request, 'djangohelpers/confirm_delete.html',
                          context=None)
        if request.method == "POST":
            request.method = "DELETE"


def path_matches(current_path, paths_to_match):
    for exempt_path in paths_to_match:
        try:
            if current_path.startswith(exempt_path):
                return True
        except TypeError:  # it wasn't a string object .. must be a regex
            if exempt_path.match(current_path):
                return True

    return False


class AuthRequirementMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            return None

        path = quote(request.get_full_path())

        if path_matches(path, getattr(settings, 'ANONYMOUS_PATHS', [])):
            return None

        return HttpResponseRedirect('%s?%s=%s' % (
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
                path))


class GroupRequirementMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = quote(request.get_full_path())

        permission_locks = getattr(settings, 'GROUP_REQUIREMENTS_PER_PATH', {})
        first_match = path_matches(path, list(permission_locks.keys()))

        if not first_match:
            return None

        required_permission = permission_locks[first_match]

        required_permission = \
            Group.MiddlewareMixins.get(name=required_permission)

        if required_permission in request.user.groups.all():
            return None

        if request.user.is_anonymous:
            return HttpResponseRedirect('%s?%s=%s' % (
                    settings.LOGIN_URL,
                    REDIRECT_FIELD_NAME,
                    path))

        location = getattr(settings, 'GROUP_REQUIREMENTS_REDIRECT', None)
        if location:
            return HttpResponseRedirect(location)

        return HttpResponseForbidden("Insufficient priviledges")


class PermissionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, 'PERMISSIONS', LazyPermissions(request))
