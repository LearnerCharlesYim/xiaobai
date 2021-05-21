# -*- coding:utf-8 -*-
# @Time   :2021/5/21 16:06
# @Author :CharlesYim
# @File   :context_processors.py
from .models import Admin

def cmsadmin(request):
    admin_id = request.session.get("admin_id")
    admin = Admin.objects.filter(pk=admin_id).first()
    if admin:
        return {'cmsuser': admin}
    else:
        return {}