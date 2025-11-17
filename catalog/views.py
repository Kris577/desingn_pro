from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from .forms import ApplicationForm
from django.contrib.auth import login

class index(generic.ListView):
    model = Application
    template_name = 'index.html'
    context_object_name = 'completed_applications'

    def index(request):
        return Application.objects.filter(status='completed').order_by('-created_at')[:4]

class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

def logout_view(request):
    logout(request)
    return redirect('index')

class ApplicationCreate(LoginRequiredMixin, generic.CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'create_application.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
