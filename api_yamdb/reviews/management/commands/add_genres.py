import csv
from django.conf import settings
from reviews.models import Genre
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/static/data/genre.csv', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if count > 0:
                    Genre.objects.get_or_create(
                        id = row[0],
                        name=row[1],
                        slug=row[2],
                    )
                count+=1
            self.stdout.write(self.style.SUCCESS('Данные загружены в БД'))