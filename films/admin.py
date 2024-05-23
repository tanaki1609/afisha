from django.contrib import admin
from .models import Film, Director, Tag, Review

# Register your models here.

admin.site.register(Film)
admin.site.register(Director)
admin.site.register(Tag)
admin.site.register(Review)
