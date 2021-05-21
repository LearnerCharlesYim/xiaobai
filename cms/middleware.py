# -*- coding:utf-8 -*-
# @Time   :2021/5/21 16:08
# @Author :CharlesYim
# @File   :middleware.py
from .models import Admin


def admin_middleware(get_response):
    # 这个中间件初始化的代码

    def middleware(request):
        # request到达view的执行代码
        admin_id = request.session.get("admin_id")
        user = Admin.objects.filter(pk=admin_id).first()
        if user:
            request.admin = user
        else:
            request.admin = None

        response = get_response(request)

        # response到达浏览器的执行代码

        return response

    return middleware