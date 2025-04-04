from django.db import models
from django.utils import timezone


class Director(models.Model):
    fio = models.CharField(max_length=255)
    birthday_date = models.DateField()

    def __str__(self):
        return self.fio

    def age(self):
        return timezone.now().year - self.birthday_date.year


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Film(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE,
                                 null=True, blank=True)  # director_id
    genres = models.ManyToManyField(Genre, blank=True)
    name = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    kp_rating = models.FloatField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # noinspection PyPropertyDefinition
    @property
    def genre_names(self):
        return [i.name for i in self.genres.all()]


STARS = (
    (i, '* ' * i) for i in range(1, 11)
)


class Review(models.Model):
    text = models.TextField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE,
                             related_name='reviews')
    stars = models.IntegerField(default=10, choices=STARS)

    def __str__(self):
        return self.text
