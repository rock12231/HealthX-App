import logging
from Profile.models import UserActivityLog
from django.shortcuts import redirect

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #   if request.path.startswith('/admin/'):
        if request.path.endswith('/logout/'):
            return self.get_response(request)
        if request.user.is_authenticated:
            response = self.get_response(request)
            # Capture user activity
            user = request.user
            activity = f"Endpoint: {request.path}, Method: {request.method}"
            # Log the user activity
            log_entry = UserActivityLog(user=user, activity=activity)
            log_entry.save()
            return response
        if request.user.is_anonymous and (request.path == '/login/' or request.path == '/register/' or request.path == '/'):
            return self.get_response(request)
        else:
            return redirect('home')

