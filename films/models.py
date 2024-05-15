from datetime import datetime

from django.db import models


# Create your models here.

class Film(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.FloatField()
    is_active = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def created_date(self):
        return f'{self.created.month}/{self.created.day}/{self.created.year}'
