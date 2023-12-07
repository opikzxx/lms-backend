from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Enrollment
from library.helper.interface import response

def validate_enrollment():
    def decorator(func):
        def wrapped_view(request, *args, **kwargs):
            user = request.user
            batch_id = kwargs.get('batch_id')
            
            try:
                enrollment = Enrollment.objects.get(user=user, course_batch__id=batch_id)
            except Enrollment.DoesNotExist:
                return Response(response(403, "User has no access to the course", None, "Not Enrolled to the course"), status=status.HTTP_403_FORBIDDEN)
            
            return func(request, *args, enrollment=enrollment, **kwargs)
        
        return wrapped_view
    return decorator
