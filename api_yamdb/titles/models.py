from django.db import models


class Categories(models.Model):
    category = models.CharField(
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )


class Titles(models.Model):
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        verbose_name='Произведение',
        related_name='titles',
    )
    name = models.CharField(
        unique=True
    )
    year = models.IntegerField(
        verbose_name='Год создания'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.SET_NULL,
        verbose_name='Жанр',
        related_name='genre',
    )
