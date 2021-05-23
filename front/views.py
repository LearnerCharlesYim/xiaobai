from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import User,Certificate,Comments,Jobtype,Offer
from cms.models import Banner,News
import os

# Create your views here.

def index(request):
    banners = Banner.objects.order_by('-priority').all()[:4]
    offers = Offer.objects.order_by('-pub_time')[:3]
    return render(request,'front/index.html',context={'banners':banners,'offers':offers})


@require_http_methods(["POST"])
def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    role = request.POST.get('role')
    if not User.objects.filter(username=username):
        user = User(username=username, password=password,role=int(role))
        user.save()
        return JsonResponse({'code': 200, 'message': '注册成功'})
    else:
        return JsonResponse({'code': 400, 'message': '用户名已存在'})

@require_http_methods(["POST"])
def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    user = User.objects.filter(username=username, password=password).first()
    if user:
        if user.is_active:
            request.session['user_id'] = user.id
            if remember:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)
            return JsonResponse({'code': 200, 'message': '登录成功'})
        else:
            return JsonResponse({'code': 400, 'message': '用户被禁用，请联系管理员'})
    else:
        return JsonResponse({'code': 400, 'message': '用户名或密码错误'})

@require_http_methods(['GET'])
def logout(request):
    request.session.flush()
    return redirect(reverse('index'))

def profile(request):
    user = request.frontuser
    certificate = user.certificate_set.all()
    offers = Offer.objects.filter(author=user).order_by('-pub_time').all()
    return render(request,'front/profile.html',context={'certificate':certificate,'offers':offers})


@require_http_methods(['POST'])
def upload_avatar(request):
    avatar = request.FILES.get('file')
    user = request.frontuser
    from xiaobai.settings import BASE_DIR
    path = os.path.join(BASE_DIR,'static/images')
    user.avatar = avatar.name
    user.save()
    with open(os.path.join(path,avatar.name),'wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    return JsonResponse({'code':0,'msg':avatar.name})

@require_http_methods(['POST'])
def upload_certificate(request):
    certificate = request.FILES.get('certificate')
    user = request.frontuser
    from xiaobai.settings import BASE_DIR
    path = os.path.join(BASE_DIR,'static/images')
    certificate_ = Certificate(path=certificate.name)
    certificate_.owner = user
    certificate_.save()
    with open(os.path.join(path,certificate.name),'wb') as fp:
        for chunk in certificate.chunks():
            fp.write(chunk)
    return JsonResponse({'code':0,'msg':certificate.name})

@require_http_methods(['POST'])
def settings(request):
    user = request.frontuser
    username = request.POST.get('username')
    realname = request.POST.get('realname')
    telephone = request.POST.get('telephone')
    signature = request.POST.get('signature')
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    education = request.POST.get('education')
    user.username = username
    user.realname = realname
    user.telephone = telephone
    user.signature = signature
    user.gender = int(gender) if gender else 3
    user.age = int(age) if age else None
    user.education = int(education) if education else None
    user.save()
    return JsonResponse({'code':200,'message':''})

@require_http_methods(['POST'])
def repwd(request):
    password = request.POST.get('password')
    user = User.objects.get(id=request.frontuser.id)
    user.password = password
    user.save()
    return JsonResponse({'code':200,'message':'修改成功'})

def pub_offer(request):
    if request.method == 'GET':
        jobtypes = Jobtype.objects.all()
        return render(request, 'front/puboffer.html', context={'jobtypes': jobtypes})
    else:
        title = request.POST.get('title')
        jobtype_id = request.POST.get('jobtype_id')
        desc = request.POST.get('desc')
        img = request.POST.get('img')

        offer = Offer(title=title,desc=desc,img=img,type=1 if request.frontuser.role == 1 else 2)
        offer.category = Jobtype.objects.get(id=jobtype_id)
        offer.author = request.frontuser
        offer.save()
        return JsonResponse({'code':200,'message':''})

@require_http_methods(['POST'])
def upload_res(request):
    img = request.FILES.get('file')
    from xiaobai.settings import BASE_DIR
    path = os.path.join(BASE_DIR,'static/images')

    with open(os.path.join(path,img.name),'wb') as fp:
        for chunk in img.chunks():
            fp.write(chunk)
    return JsonResponse({'code':0,'msg':img.name})


@require_http_methods(['POST'])
def del_res(request):
    data_id = request.POST.get('data_id')
    offer = Offer.objects.filter(id=data_id).first()
    offer.delete()
    return JsonResponse({'code':200,'message':''})


def edit_offer(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        offer = Offer.objects.get(id=id)
        jobtypes = Jobtype.objects.all()
        return render(request,'front/editoffer.html',context={'jobtypes':jobtypes,'offer':offer})
    else:
        id = request.POST.get('id')
        title = request.POST.get('title')
        jobtype_id = request.POST.get('jobtype_id')
        desc = request.POST.get('desc')
        img = request.POST.get('img')
        offer = Offer.objects.get(id=id)

        offer.title = title
        offer.desc = desc
        offer.img = img
        offer.category = Jobtype.objects.get(id=jobtype_id)
        offer.save()
        return JsonResponse({'code':200, 'message':''})

def zhaopin(request):
    jobtypes = Jobtype.objects.all()
    offers = Offer.objects.filter(type=1).order_by('-pub_time')
    context = {
        'jobtypes':jobtypes,
        'offers':offers
    }
    return render(request,'front/zhaopin.html', context=context)

def qiuzhi(request):
    jobtypes = Jobtype.objects.all()
    offers = Offer.objects.filter(type=2).order_by('-pub_time')
    context = {
        'jobtypes':jobtypes,
        'offers':offers
    }
    return render(request,'front/qiuzhi.html', context=context)

def news(request):
    newses = News.objects.filter(type=2).order_by('-pub_time')
    return render(request,'front/news.html',context={'newses':newses})