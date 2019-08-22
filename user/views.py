from django.shortcuts import render,redirect
# auth模块提供了很多API管理用户信息, 在必要的时候我们可以导入User表进行操作, 比如其它表需要与User建立关联时:
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate 认证用户
from django.contrib.auth import login, logout, authenticate
# 找回密码
import random
from django.contrib.auth.hashers import make_password
# Create your views here.
# 用户登录
def loginView(request):
    # 设置标题和另外两个URL链接
    title = '登录'
    unit_2 = '/user/register.html'
    unit_2_name = '立即注册'
    unit_1 = '/user/setpassword.html'
    unit_1_name = '修改密码'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            # 使用关键字参数传递账户和凭据
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                return redirect('/')
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    return render(request, 'user.html', locals())

# 用户注册
def registerView(request):
    # 设置标题和另外两个URL链接
    title = '注册'
    unit_2 = '/user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/user/setpassword.html'
    unit_1_name = '修改密码'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            tips = '用户已存在'
        else:
            # 创建用户
            user = User.objects.create_user(username=username, password=password)
            # 建立user对象，在此，需要调用save()方法才可将此新用户保存到数据库中。
            user.save()
            tips = '注册成功，请登录'
    return render(request, 'user.html', locals())

# 修改密码
def setpasswordView(request):
    # 设置标题和另外两个URL链接
    title = '修改密码'
    unit_2 = '/user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/user/register.html'
    unit_1_name = '立即注册'
    new_password = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        old_password = request.POST.get('password', '')
        new_password = request.POST.get('new_password', '')
        if User.objects.filter(username=username):
            user = authenticate(username=username,password=old_password)
            # 判断用户的账号密码是否正确
            if user:
                # 修改密码是User的实例方法, 该方法不验证用户身份
                user.set_password(new_password)
                user.save()
                tips = '密码修改成功'
            else:
                tips = '原始密码不正确'
        else:
            tips = '用户不存在'
    return render(request, 'user.html', locals())

# 使用make_password实现密码修改
from django.contrib.auth.hashers import make_password
def setpasswordView_1(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        old_password = request.POST.get('password', '')
        new_password = request.POST.get('new_password', '')
        # 判断用户是否存在 User.objects.filter查询方法
        user = User.objects.filter(username=username)
        if User.objects.filter(username=username):
            user = authenticate(username=username,password=old_password)
            # 判断用户的账号密码是否正确
            if user:
                # 密码加密处理并保存到数据库
                dj_ps = make_password(new_password, None, 'pbkdf2_sha256')
                user.password = dj_ps
                user.save()
            else:
                print('原始密码不正确')
    return render(request, 'user.html', locals())

# 找回密码
def findPassword(request):
    button = '获取验证码'
    new_password = False
    if request.method == 'POST':
        username = request.POST.get('username', 'root')
        VerificationCode = request.POST.get('VerificationCode', '')
        password = request.POST.get('password', '')
        user = User.objects.filter(username=username)
        # 用户不存在
        if not user:
            tips = '用户' + username + '不存在'
        else:
            # 判断验证码是否已发送
            if not request.session.get('VerificationCode', ''):
                # 发送验证码并将验证码写入session
                button = '重置密码'
                tips = '验证码已发送'
                new_password = True
                # 在python中的random.randint(a,b)用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限
                VerificationCode = str(random.randint(1000, 9999))
                request.session['VerificationCode'] = VerificationCode
                # email_user(subject,message,from_email=None)：
                # 发送一封邮件给这个用户，依靠的当然是该用户的email属性。如果from_email不提供的话，Django会使用settings中的DEFAULT_FROM_EMAIL发送。
                user[0].email_user('找回密码', VerificationCode)
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                tips = '密码已重置'
            # 输入验证码错误
            else:
                tips = '验证码错误，请重新获取'
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'findPassword.html', locals())

# 用户注销，退出登录
def logoutView(request):
    logout(request)
    return redirect('/')