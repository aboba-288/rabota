from django.db import models

class Vacancy(models.Model):
    title = models.CharField(unique=True, max_length=200)
    salary = models.IntegerField(blank=True, null=True)
    area = models.CharField(unique=False, max_length=200)
    published = models.DateTimeField()