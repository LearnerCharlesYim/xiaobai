# -*- coding:utf-8 -*-
# @Time   :2021/5/18 11:38
# @Author :CharlesYim
# @File   :context_processors.py.py
from .models import User

def frontuser(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(pk=user_id).first()
    if user:
        return {'frontuser': user}
    else:
        return {}