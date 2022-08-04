from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.shortcuts import render
from django.contrib import messages


from accounts.utils import *
from accounts.forms import NewUserForm, LoginForm, ValidationForm

# Create your views here.

@logout_required(redirect_url="home")
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
                
                return redirect("home")
        else:
            placeholders = {"min_length": 9, "model_name": "User", "field_label": "email"}
            process_form_errors(form.errors.as_data(), context, placeholders)

    return render(request, "accounts/register.html", context)

@logout_required(redirect_url="home")
def login_user(request: HttpRequest):
    form = LoginForm()
    context = {"form": form}

    if(request.method == "POST"):
        form:LoginForm = LoginForm(request.POST)

        if(form.is_valid()):
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if(user is not None):
                login(request, user)

                return redirect("home")
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
@group_unrequired(group_name="Verified", redirect_url="home")
def verify_user(request: HttpRequest):
    form = ValidationForm()
    context = {"form": form}
    valid: UserValidation = get_validation(request.user)

    if(valid == None):
        valid = UserValidation(user=request.user)
        valid.save()
    elif(valid.expired(30)):
        valid.generate_new_code()

    if(request.method == "POST"):
        form = ValidationForm(request.POST)
        if(form.is_valid()):
            if(form.cleaned_data["code"] == valid.code):
                group:Group = Group.objects.get(name="Verified")
                group.user_set.add(request.user)
                valid.delete()

                return redirect("test")
            else:
                messages.error(request, "The codes don't match")
        else:
            process_form_errors(form.errors.as_data(), context, {})

    if(valid.sent == False):
        sent = send_verify_email(request, valid)

        if(sent == 1):
            valid.sent = True
            valid.save()
        else:
            messages.error(request, "Can't send to given email")

    return render(request, "accounts/verify.html", context)

@login_required(login_url="login")
@group_unrequired(group_name="Verified", redirect_url="home")
def resend_verification(request: HttpRequest):
    if(request.method == "POST"):
        validation: UserValidation = get_validation(request.user)

        if(validation is not None and validation.expired(1)):
            validation.generate_new_code()
            sent = send_verify_email(request, validation)
            if(sent == 1):
                messages.success(request, "Email resent successfully")

    return redirect("verify")

def test(request):
    return HttpResponse("OK")