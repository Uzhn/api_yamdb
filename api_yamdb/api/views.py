from rest_framework import viewsets, status, serializers
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .pagination import PagePaginations
from rest_framework.response import Response

from reviews.models import Titles, Reviews

from .serializers import (ReviewsSerializer, CommentsSerializer,
                          TitlesSerializer
                          )


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer

    def get_queryset(self):
        queryset = (Titles.objects.annotate(rating=Avg('title__score')).
                    order_by('-rating'))
        return queryset


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = PagePaginations

    def select_objects(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Titles, pk=title_id)

    def get_queryset(self):
        titles = self.select_objects()
        return titles.title.all()

    # def retrieve(self, request, *args, **kwargs):
    #     titles = self.select_objects()
    #     return titles.title.all()[kwargs['pk']]

    def get_object(self):
        titles = self.select_objects()
        try:
            return titles.title.all()[int(self.kwargs.get('pk'))-1]
        except Exception as error:
            raise serializers.ValidationError("Нету такой страницы", error)

    def perform_create(self, serializer):
        new = self.select_objects()
        serializer.save(author=self.request.user, title=new)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = PagePaginations

    def select_objects(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Reviews, pk=review_id)

    def get_queryset(self):
        rev = self.select_objects()
        return rev.review.all()

    def perform_create(self, serializer):
        new = self.select_objects()
        serializer.save(author=self.request.user, review=new)
