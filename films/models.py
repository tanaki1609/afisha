import datetime

from django.db import models


class Director(models.Model):
    fio = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return self.fio

    def age(self):
        return datetime.datetime.now().year - self.year


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Film(models.Model):
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True, related_name='movies')
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=100, null=False)
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

    def director_fio(self):
        return self.director.fio

    def tag_names(self):
        return [tag.name for tag in self.tags.all()]


STARS = (
    (i, '* ' * i) for i in range(1, 11)
)


class Review(models.Model):
    text = models.TextField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=6)

    def __str__(self):
        return self.text
