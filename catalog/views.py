from django.shortcuts import render, redirect
from django.views import generic

from desing_pro.asgi import application
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from .forms import ApplicationForm
from django.contrib.auth import login

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
# --- ДОБАВЛЕНО: Импортируем классы из django.views.generic ---
from django.views.generic import ListView, CreateView, DeleteView
# ---
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404
from .models import Application, Category
from .forms import RegisterForm, ApplicationForm

def index(request):
    context = {'completed_applications': Application.objects.filter(status='completed').order_by('-created_at')[:4]}
    return render(request, 'index.html', context)

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

class Profile(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'profile.html'
    context_object_name = 'user_applications'

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.GET.get('status')
        queryset = Application.objects.filter(user=user).order_by('-created_at')

        if status_filter in ['new', 'in_progress', 'completed']:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        return context

class ApplicationDelete(generic.DeleteView):
    model = Application
    template_name = 'delete_application.html'
    success_url = reverse_lazy('profile')


# catalog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Application, Category
from .forms import RegisterForm, ApplicationForm

# Функция для проверки прав администратора
def is_admin(user):
    """Проверяет, является ли пользователь администратором (staff)."""
    return user.is_staff

def index(request):
    # Получаем последние 4 выполненные заявки
    completed_applications = Application.objects.filter(status='completed').order_by('-created_at')[:4]
    context = {'completed_applications': completed_applications}
    return render(request, 'index.html', context)

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

def logout_view(request):
    logout(request)
    return redirect('index')

class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'create_application.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class Profile(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'profile.html'
    context_object_name = 'user_applications'

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.GET.get('status')
        queryset = Application.objects.filter(user=user).order_by('-created_at')

        if status_filter in ['new', 'in_progress', 'completed']:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        return context

class ApplicationDelete(DeleteView):
    model = Application
    template_name = 'delete_application.html'
    success_url = reverse_lazy('profile')

# --- Новые представления для админ-панели (с базовыми проверками) ---

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    """Отображает главную страницу админ-панели."""
    applications = Application.objects.select_related('user', 'category').all().order_by('-created_at')
    categories = Category.objects.all()
    context = {'applications': applications, 'categories': categories}
    return render(request, 'admin_panel.html', context)

@login_required
@user_passes_test(is_admin)
def change_application_status(request):
    """Изменяет статус заявки."""
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('new_status')

        application = get_object_or_404(Application, id=application_id)
        # Проверяем, что новый статус допустим
        valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
        if new_status in valid_statuses:
            old_status_display = application.get_status_display()
            application.status = new_status
            application.save()
            messages.success(
                request,
                f'Статус заявки "{application.title}" изменён с "{old_status_display}" на "{application.get_status_display()}".'
            )
    return redirect('catalog:admin_panel')

@login_required
@user_passes_test(is_admin)
def add_category(request):
    """Добавляет новую категорию."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            # Проверяем, не существует ли уже категория с таким именем
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(name=name)
                messages.success(request, f'Категория "{name}" добавлена.')
            else:
                messages.error(request, f'Категория "{name}" уже существует.')
    return redirect('catalog:admin_panel')

@login_required
@user_passes_test(is_admin)
def delete_category(request, category_id):
    """Удаляет категорию и связанные заявки."""
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category_name = category.name
        category.delete()
        messages.success(request, f'Категория "{category_name}" и связанные заявки удалены.')