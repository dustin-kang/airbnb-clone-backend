from multiprocessing import AuthenticationError
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        # 로그아웃
        if not token:
            return None
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")

        # 잘못된 토큰의 경우
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            # 인증 성공
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            # 인증 실패(존재하지 않은 키)
            raise AuthenticationFailed("User Not Found")