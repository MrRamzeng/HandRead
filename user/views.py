from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy as url

from .forms import SignupForm
from .models import User


class RegisterView(CreateView):
    template_name = 'user/user_form.html'
    model = User
    form_class = SignupForm
    success_url = url('index')
    redirect_authentication_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Регистрация'
        return context

    def form_valid(self, form):
        valid = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterView, self).get(*args, **kwargs)


class LogView(LoginView):
    template_name = 'user/user_form.html'
    success_url = url('user_books')
    redirect_authentication_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Авторизация'
        return context


def logout_view(request):
    logout(request)
    return redirect('index')