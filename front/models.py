from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=254,unique=True)
    realname = models.CharField(max_length=254,null=True)
    password = models.CharField(max_length=18)
    telephone = models.CharField(max_length=11,null=True)
    gender = models.IntegerField(choices=((1, '男'), (2, '女'), (3, '未知')), default=3)
    age = models.IntegerField(null=True)
    education = models.IntegerField(choices=((1,'博士'),(2,'研究生'),(3,'本科'),(4,'高中'),(5,'高中及一下')),null=True)
    signature = models.TextField(null=True)
    avatar = models.CharField(max_length=254,null=True)
    role = models.IntegerField(choices=((1,'员工'),(2,'用户')))
    is_active = models.BooleanField(default=True)


class Certificate(models.Model):
    path = models.CharField(max_length=254,null=True)
    owner = models.ForeignKey('User',on_delete=models.CASCADE)


class Jobtype(models.Model):
    name = models.CharField(max_length=254)
    create_time = models.DateTimeField(auto_now_add=True)


class Offer(models.Model):
    title = models.CharField(max_length=254)
    desc = models.TextField()
    img = models.CharField(max_length=254,null=True)
    category = models.ForeignKey('Jobtype',on_delete=models.SET_NULL,null=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User',on_delete=models.CASCADE)
    type = models.IntegerField(choices=((1,'求职'),(2,'发布招聘')))


class Comments(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    offer = models.ForeignKey('Offer',on_delete=models.CASCADE)
    author = models.ForeignKey('User',on_delete=models.CASCADE)
    origin_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)