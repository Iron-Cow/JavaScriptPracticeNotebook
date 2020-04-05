from django.shortcuts import render, redirect, get_object_or_404, Http404
from .forms import ProblemForm, LanguageForm
from .models import Problem, Language
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'sketch/index.html')


def problems_list(request):
    print()
    context = dict()
    all_tasks = Problem.objects.all()
    if request.method == "GET":
        query = request.GET.get("q")
        if query:
            all_tasks = all_tasks.filter(
                Q(title__icontains=query) |
                Q(solutioncode__icontains=query) |
                Q(language__name__icontains=query) |
                Q(user__username__icontains=query) |
                Q(problemtext__icontains=query)
            ).distinct()
        form = ProblemForm()
        paginator = Paginator(all_tasks, 3)
        page_request_var = "page"
        page = request.GET.get(page_request_var)
        try:
            all_tasks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_tasks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            all_tasks = paginator.page(paginator.num_pages)
        context["page_request_var"] = page_request_var
        context['form'] = form
        context['all_tasks'] = all_tasks
        return render(request, "sketch/problems_list.html", context)
    elif request.method == "POST":
        form = ProblemForm(request.POST)
        context['form'] = form
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect(f'/problems_list')


def add_language(request):
    if not request.user.is_superuser:
        raise Http404

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


def delete_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    if not request.user.is_superuser:
        raise Http40
    language.delete()
    return redirect("/add_language")


def edit_problem(request, problem_id: int):
    context = dict()
    problem = get_object_or_404(Problem, id=problem_id)
    if not request.user.is_superuser and request.user != problem.user:
        raise Http404

    if request.method == "GET":

        form = ProblemForm(instance=problem)
        context['form'] = form
        context['problem'] = problem
        return render(request, "sketch/edit_problem.html", context)
    elif request.method == "POST":
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem.title = form.cleaned_data['title']
            problem.problemtext = form.cleaned_data['problemtext']
            problem.solutioncode = form.cleaned_data['solutioncode']
            problem.save()
        return redirect('/problems_list')


def delete_problem(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id)
    if not request.user.is_superuser and request.user != problem.user:
        raise Http40
    problem.delete()
    return redirect("/problems_list")


def js_editor(request):
    return render(request, 'sketch/codemirrortest.html')
