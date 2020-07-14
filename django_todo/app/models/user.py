from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass

    header = models.CharField(max_length=128, help_text='头像')

    def __str__(self):
        return '<User> {}'.format(self.username)
