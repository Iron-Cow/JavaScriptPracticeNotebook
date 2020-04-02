from django.shortcuts import render, redirect
from .forms import ProblemForm, LanguageForm
from .models import Problem, Language


def index(request):
    return render(request, 'sketch/index.html')


def problems_list(request):
    context = dict()
    all_tasks = Problem.objects.all()
    context['all_tasks'] = all_tasks
    if request.method == "GET":
        form = ProblemForm()
        context['form'] = form
        return render(request, "sketch/problems_list.html", context)
    elif request.method == "POST":
        form = ProblemForm(request.POST)
        context['form'] = form
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('/problems_list')


def add_language(request):
    context = dict()
    all_languages = Language.objects.all()
    context['all_languages'] = all_languages
    if request.method == "GET":
        form = LanguageForm()
        context['form'] = form
        return render(request, "sketch/add_language.html", context)
    elif request.method == "POST":
        form = LanguageForm(request.POST)
        if not all_languages.filter(name=form.data['name'].lower()).exists():
            form.save()
        return redirect('/add_language')


def js_editor(request):
    return render(request, 'sketch/codemirrortest.html')
