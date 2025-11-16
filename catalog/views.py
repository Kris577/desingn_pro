from django.shortcuts import render
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy

def index(request):
    return render(request, 'index.html')

class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
