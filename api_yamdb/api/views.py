from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .pagination import CatsPagination

from reviews.models import Titles

from .serializers import ReviewsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = CatsPagination

    def select_objects(self):
        post_id = self.kwargs.get("title_id")
        return get_object_or_404(Titles, pk=post_id)

    def get_queryset(self):
        titles = self.select_objects()
        return titles.title.all()
