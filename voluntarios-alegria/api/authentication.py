from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        token = token.replace("Token ", "") if token else None

        if token != "dm9sdW50YXJpb3MtYWxlZ3JpYQ==":
            raise AuthenticationFailed("Token inválido ou ausente.")

        return True

