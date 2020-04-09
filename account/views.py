from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, Http404
from .models import Feedback, Usersetup
from .forms import FeedbackForm, FeedbackFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


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
        active()
        return redirect('/')
    SETTINGS = Usersetup.objects.get(id=0)
    user_feedbacks = Feedback.objects.filter(user=request.user).exclude(status__in=("Deleted by user", "Ignored")).order_by('-id')
    data = dict()
    if request.user.is_active:
        quote = SETTINGS.registered_user_feedback_limit
    else:
        quote = SETTINGS.unregistered_user_feedback_limit
    data['quote'] = quote
    feedback_quote_left = quote - user_feedbacks.filter(status='Pending').count()
    data['feedback_quote_left'] = feedback_quote_left
    data['user_feedbacks'] = user_feedbacks
    if request.method == "GET":
        if request.user.is_superuser:
            data['new_users'] = User.objects.filter(is_active=False)
            data['new_feedbacks'] = Feedback.objects.filter(status='Pending')
        form = FeedbackForm()
        data['form'] = form

        return render(request, 'account/profile.html', data)
    elif request.method == "POST":
        if feedback_quote_left <= 0:
            messages.info(request, "Feedback NOT saved. Quota reached. \n"
                                   "Please wait for an answer from Admin.")
        else:
            form = FeedbackForm(request.POST)
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.info(request, "Sent successfully")
        return redirect(f'/account/profile')


def delete_feedback_by_user(request, feedback_id: int):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.user == feedback.user:
        feedback.status = "Deleted by user"
        feedback.save()
        messages.info(request, "Deleted successfully")
    return redirect('/account/profile')


def feedback_answer(request, feedback_id: int):
    if request.method == "POST" and request.user.is_superuser:
        feedback = get_object_or_404(Feedback, id=feedback_id)
        answer = request.POST.get(f"answer-{feedback_id}")
        feedback.answer = answer
        feedback.status = "Answered"
        feedback.save()
        messages.info(request, "Answered successfully")
        return redirect('/account/admin_feedback_list')


def admin_feedback_list(request):
    if not request.user.is_superuser:
        messages.info(request, "No access")
        return redirect('/account/profile')
    data = dict()
    confirmed_statuses = ['Pending', 'Answered', 'Deleted by user', 'Ignored']
    if "?" in request.get_raw_uri():
        confirmed_statuses = list(filter(lambda x: bool(request.GET.get(x)), confirmed_statuses))
    all_feedbacks = Feedback.objects.all().order_by("-id").filter(status__in=confirmed_statuses)
    data['all_feedbacks'] = all_feedbacks
    query = request.GET.get("q")
    if query:
        all_feedbacks = all_feedbacks.filter(
            Q(user__username__icontains=query) |
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(answer__icontains=query) |
            Q(status__contains=query)
        ).distinct()
        paginator = Paginator(all_feedbacks, 5)
        page_request_var = "page"
        page = request.GET.get(page_request_var)
        try:
            all_feedbacks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_feedbacks = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            all_tasks = paginator.page(paginator.num_pages)
            messages.info(request, "Too big page. Try the last one")
        data["page_request_var"] = page_request_var
        data['all_feedbacks'] = all_feedbacks

    return render(request, 'account/admin_feedback_list.html', data)


def delete_feedback_totally(request, feedback_id: int):
    if not request.user.is_superuser:
        messages.info(request, "No access")
        return redirect('/account/profile')
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    messages.info(request, "Deleted successfully")
    return redirect('/account/admin_feedback_list')


def ignore_feedback(request, feedback_id: int):
    if not request.user.is_superuser:
        messages.info(request, "No access")
        return redirect('/account/profile')
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.status = "Ignored"
    feedback.save()
    messages.info(request, "Ignored successfully")
    return redirect('/account/admin_feedback_list')


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
