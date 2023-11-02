from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        response.data = {
            'detail': 'Authorization token were not provided.',
            'code' : 'token_not_present'
        }
        response.status_code = 401  # Unauthorized status code

    return response