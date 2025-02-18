from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app_account.forms import CostumeUserCreationForm
from app_account.backends import EmailBackend
from django.contrib.auth.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('app_blog:home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            user = EmailBackend.authenticate(request, request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully')
            return redirect('app_blog:home')
        else:
            messages.error(request, 'Wrong Information')
            return redirect('app_account:login')

    return render(request, 'app_account/login.html')


def logout_view(request):
    try:
        logout(request)
        messages.success(request, 'Logout Successfully')
        return redirect('app_account:login')
    except:
        messages.error(request, 'Logout Failed')
        return redirect('app_blog:home')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('app_blog:home')
    if request.method == 'POST':
        form = CostumeUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email'])
            if user:
                messages.error(request, 'Account exists,Try Again')
                return redirect('app_account:signup')
            form.save()
            messages.success(request, 'Sign Up Successfully')
            return redirect('app_account:login')
        else:
            messages.error(request, 'Wrong Information,Try Again')
            return redirect('app_account:signup')

    return render(request, 'app_account/signup.html', {'form': CostumeUserCreationForm()})

