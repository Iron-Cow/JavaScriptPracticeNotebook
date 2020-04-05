from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Problem(models.Model):
    title = models.CharField(max_length=64)
    problemtext = models.TextField(max_length=1024)
    solutioncode = models.TextField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}. {self.title}'

    class Meta:
        ordering = ["id", ]
