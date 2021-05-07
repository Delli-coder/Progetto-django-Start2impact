from django.db import models
from django import forms
from .blockchain.utils import send_transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import hashlib


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    def write_on_chain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = send_transaction(self.hash)
        self.save()

    def set_date(self):
        self.published_date = timezone.now()
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ipAddress = models.CharField(max_length=30)
    username = models.CharField(max_length=30, default=None, null=True)

    def __str__(self):
        return self.user.username


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('user', 'content')

# Create your models here.
