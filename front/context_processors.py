# -*- coding:utf-8 -*-
# @Time   :2021/5/18 11:38
# @Author :CharlesYim
# @File   :context_processors.py.py
from .models import User
from cms.models import News

def frontuser(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(pk=user_id).first()
    if user:
        return {'frontuser': user}
    else:
        return {}

def news(request):
    announcements = News.objects.filter(type=1).order_by('-pub_time').all()[:2]
    return {'announcements':announcements}