from django.shortcuts import render, redirect

from django.http import HttpRequest, HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.urls import reverse

from accounts.utils import group_required

from quizzes.forms import NewQuizForm, NewQuestionForm, NewChoiceForm
from quizzes.utils import *
# Create your views here.

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def view_created_quizzes(request: HttpRequest):
    quizzes = Quiz.objects.filter(author=request.user)

    return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes})

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def create_quiz(request: HttpRequest):
    form = NewQuizForm()
    context = {"form": form}

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

    if(quiz.author != request.user):
        return redirect("view_quizzes") # TODO Replace this with a error template
    elif(quiz == None):
        return redirect("view_quizzes")

    form = NewQuizForm(instance=quiz)
    questions = quiz.question_set.all()
    context = {"form": form, "quiz": quiz, "questions": questions}

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

    context = {"quiz": quiz}

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

    context = {"quiz": quiz, "question": question}

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

            return redirect(reverse("modify_quiz", args=[quiz.id]))

    context = {"form": form, "quiz": quiz}
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
    quiz = question.quiz
    choices = question.choice_set.all()

    choice_forms =[]
    for choice in choices:
        choice_forms.append(NewChoiceForm(instance=choice))

    context = {"form": form, "choice_forms": choice_forms, "question": question, "quiz": quiz}

    if(request.method == "POST"):
        form = NewQuestionForm(request.POST, instance=question)
        if(form.is_valid()):
            form.save()

            return redirect("view_quizzes")

    return render(request, "quizzes/modify_question.html", context)

@login_required(login_url="login")
@group_required(group_name="Verified", redirect_url="verify")
def modify_choice(request: HttpRequest, id: int):
    print(request.POST)

    return redirect("test")