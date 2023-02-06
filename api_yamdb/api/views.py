from rest_framework import viewsets, status, serializers, filters
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .pagination import PagePaginations
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from reviews.models import Title, Review, Genre, Category
from users.models import User
from api.serializers import (AuthUserSerializer, TokenUserSerializer,
                             UserSerializer, TitlesSerializer,
                             GenresSerializer, CategoriesSerializer,
                             ReviewsSerializer, CommentsSerializer
                             )
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from api.permissions import (IsSuperUserOrIsAdmin,
                             UserAuthOrModOrAdminOrReadOnly,
                             Other)


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


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    search_fields = ('name',)
    permission_classes = (
        Other,
    )

    def get_queryset(self):
        queryset = (Title.objects.annotate(rating=Avg('title__score')).
                    order_by('-rating'))
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (
        Other,
    )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (
        Other,
    )


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = PagePaginations
    permission_classes = (
        UserAuthOrModOrAdminOrReadOnly,
    )

    def select_objects(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        titles = self.select_objects()
        return titles.title.all()

    # def retrieve(self, request, *args, **kwargs):
    #     titles = self.select_objects()
    #     return titles.title.all()[kwargs['pk']]

    # def get_object(self):
    #     titles = self.select_objects()
    #     try:
    #         return titles.title.all()[int(self.kwargs.get('pk'))-1]
    #     except Exception as error:
    #         raise serializers.ValidationError("Нету такой страницы", error)

    def perform_create(self, serializer):
        new = self.select_objects()
        serializer.save(author=self.request.user, title=new)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = PagePaginations
    permission_classes = (
        UserAuthOrModOrAdminOrReadOnly,
    )

    def select_objects(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        rev = self.select_objects()
        return rev.review.all()

    def perform_create(self, serializer):
        new = self.select_objects()
        serializer.save(author=self.request.user, review=new)
