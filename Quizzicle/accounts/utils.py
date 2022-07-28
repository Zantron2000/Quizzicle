from django.http import HttpRequest

from django.contrib.auth.models import Group

from django.shortcuts import redirect

def group_required(group_name, redirect_url):
    def inner_function(func):
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            required_group = Group.objects.get(name=group_name)
            if(not required_group in request.user.groups.all()):
                return redirect(redirect_url)
            
            return func(*args, **kwargs)
        return wrapper
    return inner_function

def logout_required(redirect_url):
    def inner_function(func):
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            if(request.user.is_authenticated):
                
                return redirect(redirect_url)
            
            return func(*args, **kwargs)
        return wrapper
    return inner_function

def group_unrequired(group_name, redirect_url):
    def inner_function(func):
        def wrapper(*args, **kwargs):
            request: HttpRequest = args[0]
            required_group = Group.objects.get(name=group_name)
            if(required_group in request.user.groups.all()):
                return redirect(redirect_url)
            
            return func(*args, **kwargs)
        return wrapper
    return inner_function

def process_form_errors(errorsDict, contextDict, placeholders={}):
    for key in errorsDict.keys():
        issues = []

        for problem in errorsDict[key]:
            if('%' in problem.message):
                print(problem.message)
                issues.append(problem.message % placeholders)
            else:
                issues.append(problem.message)

        contextDict[key] = issues