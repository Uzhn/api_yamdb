from django.db import models


class Titles(models.Model):
    category = models.ForeignKey(
        Categories,
        on_delete = models.SET_NULL,
        verbose_name='Произведение',
        related_name='titles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete = models.SET_NULL,
        verbose_name='Жанр',
        related_name='title_genre',
    )
    name = models.CharField(
        unique=True
    )
    year = models.IntegerField(
        verbose_name='Год создания'
    )

    def __str__(self):
        return self.name
