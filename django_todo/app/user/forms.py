from django import forms


class ProfileForm(forms.Form):
    picture = forms.ImageField(label='图片')
