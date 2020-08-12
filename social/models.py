from django.db import models
from django.contrib.auth.models import User
from django import forms

class Interest(models.Model):
    label = models.CharField(max_length=30,primary_key=True)

class UserInfoManager(models.Manager):
    def create_user_info(self, username, password):
        user = User.objects.create_user(username=username,
                                    password=password)
        userinfo = self.create(user=user)
        return userinfo

class UserInfo(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    objects = UserInfoManager()
    employment = models.CharField(max_length=30,default='Unspecified')
    location = models.CharField(max_length=50,default='Unspecified')
    birthday = models.DateField(null=True,blank=True)
    interests = models.ManyToManyField(Interest)
    friends = models.ManyToManyField('self')
