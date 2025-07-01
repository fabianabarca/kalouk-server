from django.db import models

# Create your models here.


class Dataset(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, primary_key=True)
    payload = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name
