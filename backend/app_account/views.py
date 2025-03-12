from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app_account.forms import CostumeUserCreationForm, LoginForm
from django.views import View
from app_account.backends import EmailBackend
from django.contrib.auth.models import User


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = "app_account/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "welcome!")
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("app_blog:home")
            else:
                messages.error(request, "wrong information")
                return redirect("app_account:login")
        else:
            messages.error(request, "wrong information")
            return redirect("app_account:login")


class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
            messages.success(request, "logout successfully!")
            return redirect("app_account:login")
        except:
            messages.error(request, "logout failed!")
            return redirect("app_account:home")


# def signup_view(request):
#     if request.user.is_authenticated:
#         return redirect('app_blog:home')
#     if request.method == 'POST':
#         form = CostumeUserCreationForm(request.POST)
#         if form.is_valid():
#             user = User.objects.filter(email=form.cleaned_data['email'])
#             if user:
#                 messages.error(request, 'Account exists,Try Again')
#                 return redirect('app_account:signup')
#             form.save()
#             messages.success(request, 'Sign Up Successfully')
#             return redirect('app_account:login')
#         else:
#             messages.error(request, 'Wrong Information,Try Again')
#             return redirect('app_account:signup')
#
#     return render(request, 'app_account/signup.html', {'form': CostumeUserCreationForm()})
