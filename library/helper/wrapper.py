from rest_framework.response import Response
from rest_framework import status

def validate_serializer(serializer_class):
    def decorator(func):
        def wrapped_view(request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = serializer.validated_data
            
            return func(request, data, *args, **kwargs)
        
        return wrapped_view
    return decorator