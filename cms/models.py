from django.db import models

# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=24)

class News(models.Model):
    title = models.CharField(max_length=254)
    content = models.TextField()
    type = models.IntegerField(choices=((1,'公告'),(2,'培训文章')))
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Admin',on_delete=models.SET_NULL,null=True)

class Banner(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=254)
    priority = models.IntegerField()