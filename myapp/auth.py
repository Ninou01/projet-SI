from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from myapp.validations import validateLogin
from .decorators import unauthenticated_user

User = get_user_model()

@unauthenticated_user
def Login(request): 
    if request.POST:
        is_valid, errors = validateLogin(request.POST)

        if is_valid: 
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect('/')
        else: 
            return render(request, 'login.html', {"errors": errors})
    
    return render(request, 'login.html')

@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    return redirect('/login/')

