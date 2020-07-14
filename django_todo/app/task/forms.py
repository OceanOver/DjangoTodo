from django import forms
from ..models.task import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['content', 'expire_time', 'user_id']
