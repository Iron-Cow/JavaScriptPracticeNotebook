from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect


def index(request):
    pass


def signup(request):
    if request.method == "GET":
        return render(request, 'account/register.html')
    elif request.method == "POST":
        login = request.POST.get('login')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        email = request.POST.get('email')

        # get data from registration form
        data = dict()

        if pass1 != pass2:
            messages.info(request, 'Passwords not equal')
            return redirect(request.get_raw_uri())
        elif User.objects.filter(username=login).exists():
            messages.info(request, 'Username is not available')
            return redirect(request.get_raw_uri())
        else:
            user = User.objects.create_user(login, email, pass1)
            user.is_active = False
            user.save()
            # Формирование отчета о результатах попытки регистрации:
            messages.info(request, 'Registration successfull. Please wait for Admin authorization.')
            return redirect('/')


def ajax_reg(request):
    response = dict()
    _login = request.GET.get('login')

    try:
        User.objects.get(username=_login)
        response['mess'] = 'occupied'
    except User.DoesNotExist:
        response['mess'] = 'free'

    # print(JsonResponse(response))
    # print(response)
    # print(request)
    return JsonResponse(response)


def signin(request):
    if request.method == "GET":
        return render(request, "account/login.html")
    elif request.method == "POST":
        data = dict()

        _login = request.POST.get('login')
        _password = request.POST.get('pass')

        data['User_name'] = _login
        data['password'] = _password
        print(_login, _password)

        # Authentication
        user = authenticate(request, username=_login, password=_password)

        if user is not None:  # if not None - username and password valid
            login(request, user)
            messages.info(request, 'Logged in successfully.')
            if not user.is_active:
                messages.info(request, 'You still cannot create your own posts before Admin permission. '
                                       'Please wait for the authentication.')
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials.')
            return redirect(request.get_raw_uri())


def signout(request):
    if request.user.is_authenticated:
        messages.info(request, 'Logged out successfully')

        logout(request)
    return redirect('/')


def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Log in first, please')
        return redirect('/')
    data = dict()
    if request.user.is_superuser:
        data['new_users'] = User.objects.filter(is_active=False)
    return render(request, 'account/profile.html', data)


def leave_feedback(request):
    pass


def feedbacks(request):
    pass


def users(request):
    if not request.user.is_superuser:
        messages.info(request, 'No access')
        return redirect('/')
    data = dict()
    userslist = User.objects.all().order_by('is_active')
    data['userlist'] = userslist
    return render(request, 'account/users.html', data)


def confirm_user(request, user_id: int):
    if not request.user.is_superuser:
        messages.info(request, 'No access')
        return redirect('/')
    user = User.objects.filter(id=user_id)
    if user.exists():
        for u in user:
            u.is_active = True
            u.save()
        messages.info(request, 'User Activated')
    return redirect('/account/users')


def deactivate_user(request, user_id: int):
    if not request.user.is_superuser:
        messages.info(request, 'No access')
        return redirect('/')
    user = User.objects.filter(id=user_id)
    if user.exists():
        for u in user:
            u.is_active = False
            u.save()
        messages.info(request, 'User Deactivated')
    return redirect('/account/users')
