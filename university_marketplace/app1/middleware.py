# app1/middleware.py

from django.shortcuts import redirect

class HTTPSRedirectMiddleware:
    """
    Redirect all HTTP requests to HTTPS,
    but let the /healthz/ probe through unmolested.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1) Allow health‐check probes over HTTP
        if request.path == "/healthz/":
            return self.get_response(request)

        # 2) Otherwise, redirect any non‐secure request
        if not request.is_secure():
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace("http://", "https://", 1)
            return redirect(secure_url, permanent=True)

        # 3) Normal request over HTTPS
        return self.get_response(request)
