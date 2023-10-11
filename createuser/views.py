from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .forms import createUserForm

def createUser(request):
    # Check if the user is already authenticated and log them out
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.createAndLogin(request) 
            return HttpResponseRedirect("/courses/user_page/") 
    form = createUserForm()

    return render(request, 'users/signup.html', {"form": form})

