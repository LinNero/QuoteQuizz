from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
import random
import distutils
from distutils import util
from django.db.models import Q

from .models import Category, QuestionSet, Question, UsersQuestions


def homepage(request):
    categories = Category.objects.order_by('id').all()
    return render(request=request, template_name="quiz/homepage.html", context={'categories': categories})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("quiz:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="quiz/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("quiz:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="quiz/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("quiz:homepage")


def show_category(request, id):
    # category = Category.objects.filter(id=id)
    question_sets = QuestionSet.objects.filter(category_id=id)
    return render(request=request, template_name="quiz/category.html", context={"question_sets": question_sets, "category_id": id})


def category_next_question(request, id):
    category = Category.objects.get(pk=id)
    question_list = []

    if request.user.__class__.__name__ == 'AnonymousUser':
        answered_questions_list = []
    else:
        answered_questions_list = UsersQuestions.objects.filter(user=request.user).values_list('question_id')

    for qs in category.question_sets.all():
        question_list += qs.questions.filter(~Q(pk__in=answered_questions_list)).values_list('pk')

    question = Question.objects.filter(~Q(pk__in=answered_questions_list)).get(pk=random.choice(question_list)[0])
    return render(request=request, template_name="quiz/question.html", context={"question": question, "category": category})


def profile(request):
    users_questions = UsersQuestions.objects.filter(user_id=request.user.id)
    category_stats = {}
    for uq in users_questions:
        category = uq.question.quote_id.source.category_id
        category_stats[category.name] = category_stats.get(category.name, {})
        if uq.is_correct:
            category_stats[category.name]['correct'] = category_stats[category.name].get('correct', 0) + 1
        else:
            category_stats[category.name]['incorrect'] = category_stats[category.name].get('incorrect', 0) + 1

    return render(request=request, template_name="quiz/profile.html",
                  context={"category_stats": category_stats})


def answer(request):
    question = Question.objects.get(pk=request.POST['question_id'])
    boolean_value = bool(distutils.util.strtobool(request.POST['is_correct']))
    users_questions = UsersQuestions(question=question, user=request.user, is_correct=boolean_value)
    users_questions.save()

    response = {'saved': True}
    return JsonResponse(response)