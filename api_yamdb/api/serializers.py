from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from reviews.models import Reviews, Comments, Titles


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews

    def validate(self, data):
        if 'POST' in self.context.get('request').method:
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Titles, pk=title_id)
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
