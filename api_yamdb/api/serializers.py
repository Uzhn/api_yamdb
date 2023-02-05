from rest_framework import serializers

from users.models import User
from reviews.models import Category, Genre, Title


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

    class Meta:
        model = Title
        fields = '__all__'
