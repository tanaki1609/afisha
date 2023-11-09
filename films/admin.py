from django.contrib import admin
from .models import Film, Director, Genre, Review

# Register your models here.

admin.site.register(Film)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Review)
