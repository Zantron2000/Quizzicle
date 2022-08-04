from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpRequest, HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.urls import reverse

from accounts.utils import group_required

from quizzes.forms import NewQuizForm, NewQuestionForm, NewChoiceForm, SearchForm
from quizzes.utils import *
# Create your views here.

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def view_created_quizzes(request: HttpRequest):
    quizzes = Quiz.objects.filter(author=request.user)
    search_form = SearchForm()
    search_form.make_mini_form()

    return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes, "search_form": search_form})

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def create_quiz(request: HttpRequest):
    form = NewQuizForm()
    search_form = SearchForm()
    search_form.make_mini_form()

    context = {"form": form, "search_form": search_form}

    if(request.method == "POST"):
        form = NewQuizForm(request.POST)
        if(form.is_valid()):
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()

            return redirect(reverse("create_question", args=[quiz.id]))

    return render(request, "quizzes/create_quiz.html", context)

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def modify_quiz(request: HttpRequest, id: int):
    quiz: Quiz = get_quiz(id)

    if(quiz == None):
        return redirect("view_quizzes")
    elif(quiz.author != request.user):
        return redirect("view_quizzes") # TODO Replace this with a error template
    

    form = NewQuizForm(instance=quiz)
    search_form = SearchForm()
    search_form.make_mini_form()
    questions = quiz.question_set.all()
    context = {"form": form, "quiz": quiz, "questions": questions, "search_form": search_form}

    if(request.method == "POST"):
        form = NewQuizForm(request.POST, instance=quiz)
        if(form.is_valid()):
            form.save()

            return redirect("view_quizzes")

    return render(request, "quizzes/modify_quiz.html", context)

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def delete_quiz(request: HttpRequest, id: int):
    quiz: Quiz = get_quiz(id)

    if(quiz.author != request.user):
        return redirect("view_quizzes") # TODO Replace this with a error template
    elif(quiz == None):
        return redirect("view_quizzes")

    search_form = SearchForm()
    search_form.make_mini_form()
    context = {"quiz": quiz, "search_form": search_form}

    if(request.method == "POST"):
        quiz.delete()
        return redirect("view_quizzes")

    return render(request, "quizzes/delete_quiz.html", context)

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def delete_question(request: HttpRequest, id: int):
    question: Question = get_question(id)
    
    if(question == None):
        return redirect("view_quizzes") # TODO Replace this with a error template get_object_or_404?
    
    quiz: Quiz = question.quiz

    if(quiz.author != request.user):
        return redirect("view_quizzes") # TODO Replace this with a error template
    elif(quiz == None):
        return redirect("view_quizzes")

    search_form = SearchForm()
    search_form.make_mini_form()
    context = {"quiz": quiz, "question": question, "search_form": search_form}

    if(request.method == "POST"):
        question.delete()
        return redirect(reverse("modify_quiz", args=[question.quiz.id]))

    return render(request, "quizzes/delete_question.html", context)

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def create_question(request: HttpRequest, id: int):
    form = NewQuestionForm()
    quiz = get_quiz(id)

    if(quiz == None):
        return redirect("view_quizzes") #TODO Replace with error template
    elif(quiz.author != request.user):
        return redirect("view_quizzes") #TODO replace with error template

    if(request.method == "POST"):
        form = NewQuestionForm(request.POST)
        if(form.is_valid()):
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()

            return redirect(reverse("modify_question", args=[question.id]))

    search_form = SearchForm()
    search_form.make_mini_form()
    context = {"form": form, "quiz": quiz, "search_form": search_form}
    return render(request, "quizzes/create_question.html", context)

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def modify_question(request: HttpRequest, id: int):
    question: Question = get_question(id)

    if(question == None):
        return redirect("view_quizzes") #TODO replace this with an error template
    elif(question.quiz.author != request.user):
        return redirect("view_quizzes") # TODO Replace this with a error template

    form = NewQuestionForm(instance=question)
    search_form = SearchForm()
    search_form.make_mini_form()
    quiz = question.quiz
    choices = question.choice_set.all()

    choice_forms =[]
    for choice in choices:
        choice_forms.append(NewChoiceForm(instance=choice))

    choices_and_forms = zip(choices, choice_forms)

    if(request.method == "POST"):
        form = NewQuestionForm(request.POST, instance=question)
        if(form.is_valid()):
            form.save()

    context = {"form": form, "choices": choices_and_forms, "question": question, "quiz": quiz, "search_form": search_form}

    return render(request, "quizzes/modify_question.html", context)

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def modify_choice(request: HttpRequest, id: int):
    choice:Choice = get_object_or_404(Choice, id=id)
    question:Question = choice.question
    quiz:Quiz = question.quiz

    if(request.user != quiz.author):
        return redirect("view_quizzes") #TODO replace with error template

    if(request.method == "POST"):
        if(request.POST.get("delete", False)):
            choice.delete()
        elif(request.POST.get("update", False)):
            form = NewChoiceForm(request.POST, instance=choice)
            if(form.is_valid()):
                form.save()

    return redirect(reverse("modify_question", args=[question.id]))

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def create_choice(request: HttpRequest, id: int):
    form = NewChoiceForm()
    question = get_object_or_404(Question, id=id)
    quiz = question.quiz

    if(quiz == None):
        return redirect("view_quizzes") #TODO Replace with error template
    elif(quiz.author != request.user):
        return redirect("view_quizzes") #TODO replace with error template

    if(request.method == "POST"):
        form = NewChoiceForm(request.POST)
        if(form.is_valid()):
            choice = form.save(commit=False)
            choice.question = question
            choice.save()

            return redirect(reverse("modify_question", args=[question.id]))

    search_form = SearchForm()
    search_form.make_mini_form()
    context = {"form": form, "question": question, "search_form": search_form}
    return render(request, "quizzes/create_choice.html", context)

def get_home(request: HttpRequest):
    search_form = SearchForm()
    search_form.make_mini_form()
    context = {"search_form": search_form}

    return render(request, "quizzes/home.html", context)

def get_search_results(request: HttpRequest):
    form = SearchForm()
    quizzes = Quiz.objects.all()
    search_form = SearchForm()
    search_form.make_mini_form()
    
    if(request.method == "GET"):
        form = SearchForm(request.GET)
        if(form.is_valid()):
            search_parameters = form.cleaned_data
            if(search_parameters.get("name", "")):
                quizzes = quizzes.filter(name__contains=search_parameters["name"])
            if(search_parameters.get("subject", "NA") != "NA" and search_parameters.get("subject", "NA")):
                quizzes = quizzes.filter(subject=search_parameters["subject"])
            if(search_parameters.get("specific_subject", "")):
                quizzes = quizzes.filter(specific_subject__contains=search_parameters["specific_subject"])
            if(search_parameters.get("author", "")):
                quizzes = quizzes.filter(author__username__contains=search_parameters["author"])

    quizzes = [quiz for quiz in quizzes if quiz.valid_questions > 0]
    context = {"form": form, "quizzes": quizzes, "search_form": search_form}
    
    return render(request, "quizzes/search_results.html", context)

def prepare_quiz(request: HttpRequest, id: int):
    search_form = SearchForm()
    search_form.make_mini_form()

    quiz = get_object_or_404(Quiz, id=id)

    if(quiz.valid_questions <= 0):
        return redirect("home")

    context = {"search_form": search_form, "quiz": quiz}
    return render(request, "quizzes/start_quiz.html", context)

def take_quiz(request: HttpRequest, id: int):
    valid_questions = []
    valid_choices = []

    search_form = SearchForm()
    search_form.make_mini_form()

    quiz: Quiz = get_object_or_404(Quiz, id=id)
    if(quiz.valid_questions <= 0):
        return redirect("home")

    for question in quiz.question_set.all():
        if(question.answerable):
            valid_questions.append(question)
            valid_choices.append(question.choice_set.all())

    context = {"search_form": search_form, "quiz": quiz, "questions_and_choices": zip(valid_questions, valid_choices)}
    return render(request, "quizzes/quiz.html", context)

def get_results(request: HttpRequest, id: int):
    quiz: Quiz = get_object_or_404(Quiz, id=id)
    data: QuizData = get_quiz_data(request.user, quiz)
    scores = []
    temp_score = None

    if(request.user.is_authenticated and data is None):
        data = QuizData(user=request.user, quiz=quiz)
        data.save()
    elif(data is not None):
        scores = data.score_set.all().order_by('-time')
    
    if(request.method == "POST"):
        score = process_test(quiz, request.POST)

        if(request.user.is_authenticated):
            attempt = Score(score=score, takenQuiz=data)
            attempt.save()
            return redirect(reverse("results", args=[id]))
        else: 
            temp_score = score

    context = {"quiz": quiz, "scores": scores, "temp_score": temp_score}
    return render(request, "quizzes/quiz_results.html", context)