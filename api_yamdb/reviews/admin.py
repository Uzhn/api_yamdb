from django.contrib import admin

from reviews.models import Category, Genre, Title, Reviews, Comments


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class TitlesAdmin(admin.ModelAdmin):
    list_display = ("pk", "category", "name", "year", "description")
    empty_value_display = "-пусто-"


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "author", "score", "pub_date", "title")
    empty_value_display = "-пусто-"


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "author", "review", "pub_date")
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoriesAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Comments, CommentsAdmin)
