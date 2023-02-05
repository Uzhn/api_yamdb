import csv
from django.conf import settings
from reviews.models import Category, Genre, Title
from django.core.management.base import BaseCommand, CommandError
from users.models import User


TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Reviews: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for table, doc in TABLES.items():
            with open(f'{settings.BASE_DIR}/static/data/{doc}', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                table.objects.bulk_create(table(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные загружены в БД'))


