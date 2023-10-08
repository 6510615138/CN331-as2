from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginInputForm
from django.contrib import messages
from .models import Scholar 
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, 'courses/user_page.html',{
                'username' : request.user, 'admin': request.user.is_staff,})
        
        scholar_user = Scholar.objects.get(ID=request.user)
        return render(request, 'courses/user_page.html',{
                'username' : scholar_user.ID, 'admin': request.user.is_staff,
                'name' : scholar_user.get_name(), 'email' : scholar_user.get_email()})
    
    if request.method == 'GET':
        return render(request, 'users/login.html', {'form' : LoginInputForm()})

    elif request.method == 'POST':
        form = LoginInputForm(request.POST)
        if form.is_valid() :
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                messages.error(request, "Invalid username or password !")
                return render(request, 'users/login.html',{
                    'form' : form, 'messages' : messages.get_messages(request)})
            
            if user.is_staff:
                login(request, user)
                return render(request, 'courses/user_page.html', {
                    'username' : user, 'admin' : request.user.is_staff,})
            
            else:
                scholar = Scholar.objects.get(ID = user)
                login(request, user)
                return render(request, 'courses/user_page.html', {
                    'username' : scholar.ID, 'admin' : request.user.is_staff,
                    'name' : scholar.get_name(), 'email' : scholar.get_email(),})
          
        
        messages.error(request, "Invalid username or password !")
        return render(request,'users/login.html',{'form' : form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login_view') 