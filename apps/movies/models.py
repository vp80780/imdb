from django.db import models
import uuid
# Create your models here.


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre = models.CharField(max_length=200, blank=True, null=True)

    # def __str__(self):
    #     return '{}'.format(self.genre)


class Movies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    director = models.CharField(max_length=250)
    genre = models.ManyToManyField(Genre)
    imdb_score = models.FloatField()
    popularity = models.FloatField()

    # def __str__(self):
    #     return '{}'.format(self.name)
