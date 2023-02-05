from rest_framework import serializers
from reviews.models import Category, Genre, Title


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
