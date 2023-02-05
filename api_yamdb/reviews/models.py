from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name = 'Слаг'
    )
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )
    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
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
