from django.db import models
from django import forms
from captcha.fields import CaptchaField
class kwejkForm(forms.Form):
    url=forms.CharField(widget=forms.URLInput,label='Url do galerii',required=True)
    def __str__(self):return self.url

class requestForm(forms.Form):
    page=forms.CharField(widget=forms.URLInput,label="nazwa strony",required=True)
    text=forms.CharField(widget=forms.Textarea, label="extra info",required=False)
    captcha=CaptchaField(required=True)

class Gallery(models.Model):
    url=models.URLField()
    name=models.CharField(max_length=1000, default="brak nazwy")
    source=models.TextField()
    def __str__(self):return self.url

class Request(models.Model):
    page=models.URLField()
    text=models.TextField()

    def __str__(self):
        return "Page: "+self.page+", extra: "+self.text