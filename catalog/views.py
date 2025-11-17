from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from .forms import ApplicationForm

def index(request):
    return render(request, 'index.html')

class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

def logout_view(request):
    logout(request)
    return redirect('index')

class Application(LoginRequiredMixin, generic.CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'create_application.html'
    success_url = reverse_lazy('index')
