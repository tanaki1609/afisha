from datetime import datetime

from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def age(self):
        return datetime.now().year - self.year


class Genre(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Film(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField(null=True)
    duration = models.IntegerField(default=100)
    rating_kinopoisk = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def rating(self):
        len_ = len(self.reviews.all())
        sum_ = sum([i.stars for i in self.reviews.all()])
        if len_ > 0:
            return sum_ / len_
        return 0

    # @property
    # def all_reviews(self):
    #     return Review.objects.filter(film_id=self.id)


STARS = (
    (1, '*'),
    (2, '* ' * 2),
    (3, '* ' * 3),
    (4, '* ' * 4),
    (5, '* ' * 5),
)


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.film.title
