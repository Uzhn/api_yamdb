from rest_framework import serializers

from users.models import User
from django.shortcuts import get_object_or_404

from reviews.models import Review, Comments, Title, Category, Genre
from users.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            message = "Использовать имя 'me' запрещено"
            raise serializers.ValidationError(message)
        return data


class TokenUserSerializer(serializers.ModelSerializer):
    """Сериализатор получиения токена JWT."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role'
                  )


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='name',
        many=True,
        required=False
    )
    catergory = genre = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        many=False,
        slug_field='name',
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category'
                  )
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if 'POST' in self.context.get('request').method:
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            author = self.context.get('request').user
            if Reviews.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    'Один пользователь, один отзыв!'
                )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
