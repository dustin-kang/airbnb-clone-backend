import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated

class JWTLogin(APIView):
    def post(self, request):
        username =  request.data.get("usernmae")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username = username,
            password = password
        )
        if user:
            # 토큰이 안전한 이유 : 암호화 X, 누가 준 토큰인지 알 수 있기 때문
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256"
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})
        