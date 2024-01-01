class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR', None)
        request.user_ip = user_ip
        response = self.get_response(request)
        return response
