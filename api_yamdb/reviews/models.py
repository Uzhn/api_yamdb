from django.db import models


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )


class Titles(models.Model):
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Произведение',
        related_name='titles',
    )
    name = models.CharField(
        max_length=256,
        unique=True
    )
    year = models.IntegerField(
        verbose_name='Год создания'
    )
    description = models.TextField
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )

    def __str__(self):
        return self.name
