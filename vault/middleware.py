class SaveIpAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if request.user.is_authenticated:
            request.session['ip'] = ip
        response = self.get_response(request)
        return response
