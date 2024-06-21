# myapp/middleware.py

from django.http import HttpResponseForbidden

class IPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ips = ['127.0.0.1', '192.168.1.1']  # İzin verilen IP adresleri listesi

        client_ip = request.META.get('REMOTE_ADDR')

        if client_ip not in allowed_ips:
            return HttpResponseForbidden("Bu IP adresinden erişim izni yok.")

        response = self.get_response(request)
        return response
