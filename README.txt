Contents:

console scripts
===============

 `maketemplatetag`
 -----------------

 A small script to output a new template tag to stdout, with human readable
 phrases encouraged. Inspired by the nice prepositions in django-tagging's
 template tags.

 If djangohelpers is installed with `setup.py`, a `maketemplatetag` script
 will be provided. Otherwise, it can also be invoked directly with 
 `python djangohelpers/console_scripts.py`.

 Run `python djangohelpers/console_scripts.py` for usage information.


middleware
==========

 djangohelpers.middleware.AuthRequirementMiddleware
 --------------------------------------------------

 If enabled, it will intercept all requests that are not logged in, and
 redirect them to the login view.

 You can specify a list of anonymously-accessible URL paths (exempt from
 this middleware) with an ANONYMOUS_PATHS list in your settings.py file.

 These paths can be strings or regexes.

 Strings will be treated as URL PREFIXES to match against.

 Regexes will be matched against the URL directly.


 djangohelpers.middleware.HttpDeleteMiddleware
 ---------------------------------------------

 If enabled, it will intercept requests with a querystring key `delete`.
 GET requests will result in a confirmation form, and POST requests will
 have their REQUEST_METHOD set to DELETE.


view decorators
===============

 djangohelpers.allow_http
 ------------------------

   @allow_http("GET", "DELETE")
   def my_view(request, ...)

 Requests with an allowed REQUEST_METHOD will be passed through untouched,
 and all other requests will return HTTP 405 Method Not Allowed.


 djangohelpers.rendered_with
 ---------------------------

   @rendered_with('foo/bar.html')
   def my_view(request, ...)

 If your view function returns a dict, it will be treated as a template context
 and the template foo/bar.html will be rendered and returned.  If your view
 function returns anything besides a dict, its response will be passed through
 untouched.

 An optional mimetype parameter is also supported:

   @rendered_with('foo/bar.json', mimetype='application/json')
   def my_view(request, ...)
 

template tags
=============

 djangohelpers.templatetags.helpful_tags
 ---------------------------------------

 A small collection of template tags and filters:

 {% replace_value of 'b' with 7 in my_dict as new_dict %}

 {{my_dict|qsify}} # converts a dict into a query string

 {{sometextwithwhitespace|split}}

 {{my_dict|getitem:'b'}}

 {{value|lessthan:12}}

 {{value|greaterthan:12}}

Originally developed at the Columbia Center for New Media Teaching & Learning.
