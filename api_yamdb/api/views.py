from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import (AuthUserSerializer, TokenUserSerializer,
                             UserSerializer
                             )
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from api.permissions import IsSuperUserOrIsAdmin

from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsSuperUserOrIsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)'
    )
    def get_user_by_username(self, request, username):
        """Метод получает/редактирует данные пользователя по его username."""
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'DELETE':
            user.delete()
            message = f'Пользователь {user} удален.'
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_profile(self, request):
        """Метод получает/редактирует данные своей учетной записи."""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    """Функция регистрации пользователя."""
    serializer = AuthUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user):
    """Фунуция отправки кода подтверждения."""
    confirmation_code = default_token_generator.make_token(user)
    subject = 'YaMDB: код подтверждения'
    message = f'Ваш код для подтверждения: {confirmation_code}'
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [user.email]
    return send_mail(subject, message, from_mail, to_mail)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_for_user(request):
    """Функция получения токена."""
    serializer = TokenUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        message = 'не правильный код подтверждения'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    access_token = AccessToken.for_user(user)
    message = {'token': str(access_token)}
    return Response(message, status=status.HTTP_200_OK)