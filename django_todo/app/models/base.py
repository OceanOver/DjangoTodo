from django.db import models


class Base(models.Model):
    class Meta:
        abstract = True

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
