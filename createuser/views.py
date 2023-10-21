from django.shortcuts import render, redirect
from .forms import createUserForm
from django.contrib.auth import login

def create_user_view(request):
    # Check if the user is already authenticated and log them out
    if request.user.is_authenticated:
        return redirect('/courses/user_page/')

    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/courses/user_page/')
    else:
        form = createUserForm()

    return render(request, 'users/signup.html', {"form": form})