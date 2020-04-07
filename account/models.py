from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):

    class StatusChoice(models.TextChoices):
        PENDING = 'Pending'
        ANSWERED = 'Answered'
        DELETED_BY_USER = 'Deleted by user'
        IGNORED = 'Ignored'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    content = models.TextField(max_length=512)
    answer = models.TextField(max_length=512, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=32, choices=StatusChoice.choices, default=StatusChoice.PENDING)

    def __str__(self):
        return f'{self.id}. {self.title} ({self.user.username}/{self.timestamp})'


class Usersetup(models.Model):
    registered_user_daily_posts = models.IntegerField(default=20)
    registered_user_feedback_limit = models.IntegerField(default=10)
    unregistered_user_daily_posts = models.IntegerField(default=0)
    unregistered_user_feedback_limit = models.IntegerField(default=2)

    def __str__(self):
        return 'USER_SETTINGS'
