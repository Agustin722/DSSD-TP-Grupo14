from django.contrib.auth.backends import BaseBackend
from my_app.models.recolector import Recolector
from django.contrib.auth.hashers import check_password

class DniAuthBackend(BaseBackend):
    def authenticate(self, request, dni=None, password=None):
        try:
            user = Recolector.objects.get(dni=dni)
            if check_password(password, user.password):
                return user
        except Recolector.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Recolector.objects.get(pk=user_id)
        except Recolector.DoesNotExist:
            return None
