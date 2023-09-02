from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from validate_email_address import validate_email


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """ Регестрация пользователя,
     в ответе выводиться полученный токен для теста запросов """

    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if email:
            if not validate_email(email):
                return Response({'message': 'Неправильный формат адреса электронной почты.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'message': 'Пользователь с таким адресом электронной почты уже существует.'},
                                status=status.HTTP_400_BAD_REQUEST)

        if not username or not password:
            return Response({'message': 'Имя пользователя и пароль обязательны для регистрации.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Пользователь с таким именем уже существует.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)

        login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'message': 'Пользователь успешно зарегистрирован', 'access_token': access_token})
    else:
        return Response({'message': 'Используйте POST запрос для регистрации пользователя'})
