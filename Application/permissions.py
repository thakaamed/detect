# myapp/permissions.py

from rest_framework.permissions import BasePermission

class IPWhitelistPermission(BasePermission):
    def has_permission(self, request, view):
        allowed_ips = ['127.0.0.1', '192.168.1.1']  # İzin verilen IP adresleri listesi

        client_ip = request.META.get('REMOTE_ADDR')

        if client_ip in allowed_ips:
            return True
        else:
            return False
