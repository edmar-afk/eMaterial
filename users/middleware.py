# middleware.py
from django.shortcuts import redirect

class ValueErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ValueError) and request.path == '/login':
            return redirect('login')