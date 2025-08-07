import time
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log HTTP requests for auditing and monitoring."""
    
    def process_request(self, request):
        """Store the start time of the request."""
        request.start_time = time.time()
    
    def process_response(self, request, response):
        """Log the request details after response is generated."""
        # Calculate response time
        if hasattr(request, 'start_time'):
            response_time = time.time() - request.start_time
        else:
            response_time = 0.0
        
        # Get user information
        user = None
        is_authenticated = False
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
            is_authenticated = True
        
        # Get remote IP
        remote_ip = self.get_client_ip(request)
        
        # Get query string
        query_string = request.META.get('QUERY_STRING', '')
        
        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create log entry asynchronously to avoid blocking the response
        try:
            RequestLog.objects.create(
                method=request.method,
                path=request.path,
                query_string=query_string,
                remote_ip=remote_ip,
                user_agent=user_agent,
                response_status=response.status_code,
                response_time=response_time,
                user=user,
                is_authenticated=is_authenticated
            )
        except Exception as e:
            # Log error but don't break the response
            print(f"Error logging request: {e}")
        
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 