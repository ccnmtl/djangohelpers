from django.shortcuts import render_to_response

class HttpDeleteMiddleware(object):
    def process_request(self, request):
        if not request.GET.has_key('delete'):
            return None
        if request.method == "GET":
            return render_to_response('djangohelpers/confirm_delete.html')
        if request.method == "POST":
            request.method = "DELETE"
