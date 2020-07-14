from django.db import models
from .base import Base


# Create your models here.
class Item(Base):
    class Meta(Base.Meta):
        db_table = 'item'

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    content = models.CharField(max_length=255, help_text='内容')
    expire_time = models.DateTimeField(help_text='过期时间')
    complete_time = models.DateTimeField(help_text='完成时间', null=True)
    note = models.CharField(max_length=255, help_text='备注', null=True)
    completed = models.SmallIntegerField(help_text='是否完成', default=0)

    def __str__(self):
        return '<Item> {}'.format(self.id)
