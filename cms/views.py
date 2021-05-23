from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_http_methods
from .models import Admin,Banner,News
from front.models import User,Jobtype,Offer
from django.http import JsonResponse
# Create your views here.

def signin(request):
    if request.method == 'GET':
        return render(request,'cms/signin.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        admin = Admin.objects.filter(username=username,password=password).first()
        if admin:
            request.session['admin_id'] = admin.id
            if remember:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)
            return JsonResponse({'code': 200, 'message': ''})
        else:
            return JsonResponse({'code':400,'message':'用户名或密码错误'})

@require_http_methods(['GET'])
def logout(request):
    request.session.flush()
    return redirect(reverse('cms_signin'))

def index(request):
    if not request.admin:
        return redirect(reverse('cms_signin'))
    return render(request,'cms/index.html')


def banner(request):
    if request.method == 'GET':
        banners = Banner.objects.all()
        return render(request,'cms/banner.html',context={'banners':banners})
    else:
        name = request.POST.get('name')
        priority = request.POST.get('priority')
        path = request.POST.get('path')
        banner = Banner(name=name,priority=priority,path=path)
        banner.save()
        return JsonResponse({'code':200,'message':''})

def upload_banner(request):
    if request.method == 'POST':
        banner = request.FILES.get('file')
        from xiaobai.settings import BASE_DIR
        import os
        path = os.path.join(BASE_DIR, 'static/images/banners')
        with open(os.path.join(path, banner.name), 'wb') as fp:
            for chunk in banner.chunks():
                fp.write(chunk)
        return JsonResponse({'code': 0, 'msg': banner.name})

def edit_banner(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        priority = request.POST.get('priority')
        path = request.POST.get('path')
        banner = Banner.objects.get(id=id)
        banner.name = name
        banner.priority = priority
        banner.path = path
        banner.save()
        return JsonResponse({'code': 200, 'message': ''})

def delete_banner(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        banner = Banner.objects.get(id=id)
        banner.delete()
        return JsonResponse({'code': 200, 'message': ''})

def user_manage(request):
    front_users = User.objects.all()
    return render(request,'cms/user_manage.html',context={'front_users':front_users})

def banned_user(request):
     if request.method == 'POST':
         id = request.POST.get('id')
         user = User.objects.get(id=id)
         user.is_active = False
         user.save()
         return JsonResponse({'code':200,'message':''})


def liftbanned_user(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        return JsonResponse({'code': 200, 'message': ''})

def job_type(request):
    jobtypes = Jobtype.objects.order_by('-create_time').all()
    return render(request,'cms/job_type.html',context={'jobtypes':jobtypes})

@require_http_methods(['POST'])
def add_jobtype(request):
    name = request.POST.get('name')
    joptype = Jobtype(name=name)
    joptype.save()
    return JsonResponse({'code':200,'message':''})

@require_http_methods(['POST'])
def edit_jobtype(request):
    data_id = request.POST.get('data_id')
    name = request.POST.get('name')
    joptype = Jobtype.objects.get(id=data_id)
    joptype.name = name
    joptype.save()
    return JsonResponse({'code':200,'message':''})

@require_http_methods(['POST'])
def delete_jobtype(request):
    data_id = request.POST.get('data_id')
    joptype = Jobtype.objects.get(id=data_id)
    joptype.delete()
    return JsonResponse({'code':200,'message':''})

def news_list(request):
    newses = News.objects.filter(type=2).order_by('-pub_time').all()
    return render(request,'cms/news_list.html',context={'newses':newses})

def pub_news(request):
    if request.method == 'GET':
        return render(request,'cms/pub_news.html')
    else:
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        news = News(title=title,desc=desc,content=content,type=2)
        news.author = request.admin
        news.save()
        return JsonResponse({'code':200,'message':''})

@require_http_methods(['POST'])
def delete_news(request):
    data_id = request.POST.get('data_id')
    news = News.objects.get(id=data_id)
    news.delete()
    return JsonResponse({'code':200,'message':''})

def announcement(request):
    announcements = News.objects.filter(type=1).order_by('-pub_time').all()
    return render(request,'cms/announcement.html',context={'announcements':announcements})

def pub_announcement(request):
    if request.method == 'GET':
        return render(request,'cms/pub_announcement.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        news = News(title=title,content=content,type=1)
        news.author = request.admin
        news.save()
        return JsonResponse({'code':200,'message':''})

@require_http_methods(['POST'])
def delete_announcement(request):
    data_id = request.POST.get('data_id')
    news = News.objects.get(id=data_id)
    news.delete()
    return JsonResponse({'code':200,'message':''})

#招聘管理
def job_manage(request):
    jobs = Offer.objects.filter(type=2).order_by('-pub_time')
    return render(request,'cms/job_manage.html',context={'jobs':jobs})

#求职管理
def jobhunting_manage(request):
    jobs = Offer.objects.filter(type=1).order_by('-pub_time')
    return render(request,'cms/jobhunting_manage.html',context={'jobs':jobs})

@require_http_methods(['POST'])
def delete_job(request):
    data_id = request.POST.get('data_id')
    offer = Offer.objects.get(id=data_id)
    offer.delete()
    return JsonResponse({'code':200,'message':''})