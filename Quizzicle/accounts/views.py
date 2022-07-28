from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.shortcuts import render
from django.contrib import messages


from accounts.utils import *
from accounts.forms import NewUserForm, LoginForm

# Create your views here.

@logout_required(redirect_url="test")
def register_user(request: HttpRequest):
    form = NewUserForm()
    context = {"form": form}

    if(request.method == "POST"):
        form = NewUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])

            if(user is not None):
                login(request, user)
                
                return redirect("test")
        else:
            placeholders = {"min_length": 9, "model_name": "User", "field_label": "email"}
            process_form_errors(form.errors.as_data(), context, placeholders)

    return render(request, "accounts/register.html", context)

@logout_required(redirect_url="test")
def login_user(request: HttpRequest):
    form = LoginForm()
    context = {"form": form}

    if(request.method == "POST"):
        form:LoginForm = LoginForm(request.POST)

        if(form.is_valid()):
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if(user is not None):
                login(request, user)

                return redirect("test")
            else:
                messages.error(request, "User not found")
        else:
            process_form_errors(form.errors.as_data(), context, {})

    return render(request, "accounts/login.html", context)

@login_required(login_url="login")
def logout_user(request: HttpRequest):
    logout(request)

    return redirect("login")

@login_required(login_url="login")
@group_unrequired(group_name="Verified", redirect_url="test")
def verify_user(request: HttpRequest):


    return render(request, "accounts/verify.html")

@login_required(login_url="login")
@group_unrequired(group_name="Verified", redirect_url="test")
def resend_verification(request: HttpRequest):
    return HttpResponse("OK")

def test(request):
    return HttpResponse("OK")