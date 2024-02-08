from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users import views

urlpatterns = [
    path("token-login", obtain_auth_token), # 해당 view에 username과 password를 보내면 토큰을 받는다.
    path("jwt-login", views.JWTLogIn.as_view())    
]
